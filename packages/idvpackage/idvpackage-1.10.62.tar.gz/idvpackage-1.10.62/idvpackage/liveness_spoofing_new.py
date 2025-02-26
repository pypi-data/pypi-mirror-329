import os
import sys
import logging

import multiprocessing
try:
    # Set start method to fork on Unix systems
    multiprocessing.set_start_method('fork', force=True)
except ValueError:
    # If fork is not available (e.g., on Windows), use spawn
    pass

# Initialize PyTorch with error handling
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    
    # Check if CUDA is available and initialize it properly
    if torch.cuda.is_available():
        try:
            torch.cuda.init()
            _device = 'cuda'
        except Exception as e:
            logging.warning(f"Failed to initialize CUDA, falling back to CPU: {e}")
            _device = 'cpu'
    else:
        _device = 'cpu'
        
    # Verify PyTorch installation
    if not torch.__version__:
        raise ImportError("PyTorch version not found")
        
    # Try to import C++ extensions
    try:
        import torch._C
    except ImportError as e:
        logging.error(f"PyTorch C++ extensions not available: {e}")
        # Continue without C++ extensions - some functionality may be limited
        pass
        
except ImportError as e:
    logging.error(f"Failed to initialize PyTorch: {e}")
    raise RuntimeError(f"PyTorch initialization failed: {e}. Please reinstall PyTorch with pip install torch --force-reinstall")

import cv2
import os
import numpy as np
from deepface import DeepFace
from idvpackage.spoof_resources.MiniFASNet import MiniFASNetV1SE, MiniFASNetV2
from idvpackage.spoof_resources import transform as trans
import gc
import torch.cuda
import psutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_MAPPING = {
    'MiniFASNetV1SE': MiniFASNetV1SE,
    'MiniFASNetV2': MiniFASNetV2
}

# # Global variables for model caching
_models = {}
_image_cropper = None

def log_memory_usage():
    """Log current process memory usage"""
    process = psutil.Process()
    logger.info(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")

def cleanup_models():
    """Clean up cached models and free memory"""
    global _models, _image_cropper, _device
    
    # Clear models
    if _models:
        for model_name in list(_models.keys()):
            try:
                model = _models[model_name]
                if hasattr(model, 'cpu'):
                    model.cpu()
                if hasattr(model, 'to'):
                    model.to('cpu')
                del model
            except Exception as e:
                logger.warning(f"Error cleaning up model {model_name}: {e}")
        _models.clear()
        _models = {}
    
    # Clear image cropper
    if _image_cropper:
        try:
            del _image_cropper
            _image_cropper = None
        except Exception as e:
            logger.warning(f"Error cleaning up image cropper: {e}")
    
    # Clear CUDA cache if available
    if torch.cuda.is_available():
        try:
            # Empty CUDA cache
            torch.cuda.empty_cache()
            
            # Additional CUDA cleanup
            if hasattr(torch.cuda, 'ipc_collect'):
                torch.cuda.ipc_collect()
            
            # Reset device
            if _device == 'cuda':
                torch.cuda.reset_peak_memory_stats()
                torch.cuda.reset_accumulated_memory_stats()
        except Exception as e:
            logger.warning(f"Error cleaning up CUDA: {e}")
    
    # Multiple GC passes
    for _ in range(3):
        gc.collect()

def get_bbox(frame):
    try:
        face_objs = DeepFace.extract_faces(frame, detector_backend='mtcnn')
        if face_objs:
            biggest_face = max(face_objs, key=lambda face: face['facial_area']['w'] * face['facial_area']['h'])
            facial_area = biggest_face['facial_area']
            x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']
            bbox = [x, y, w, h]
            return bbox
        else:
            return None
    except Exception as e:
        print(f"Error in face detection: {e}")
        return None

def parse_model_name(model_name):
    info = model_name.split('_')[0:-1]
    h_input, w_input = info[-1].split('x')
    model_type = model_name.split('.pth')[0].split('_')[-1]
    scale = None if info[0] == "org" else float(info[0])
    return int(h_input), int(w_input), model_type, scale

def get_kernel(height, width):
    return ((height + 15) // 16, (width + 15) // 16)

def load_model(model_path):
    model_name = os.path.basename(model_path)
    h_input, w_input, model_type, _ = parse_model_name(model_name)
    kernel_size = get_kernel(h_input, w_input)
    
    # Initialize model on CPU to save memory
    model = MODEL_MAPPING[model_type](conv6_kernel=kernel_size).to(_device)
    
    # Load state dict with memory optimization
    state_dict = torch.load(model_path, map_location=_device)
    if next(iter(state_dict)).startswith('module.'):
        state_dict = {k[7:]: v for k, v in state_dict.items()}
    
    model.load_state_dict(state_dict)
    del state_dict
    gc.collect()
    
    model.eval()
    return model

def predict(img, model):
    test_transform = trans.Compose([trans.ToTensor()])
    img = test_transform(img).unsqueeze(0).to(_device)
    
    with torch.no_grad():
        result = model.forward(img)
        result = F.softmax(result).cpu().numpy()
    
    # Clear GPU memory if available
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    return result

def check_image(image):
    height, width, _ = image.shape
    
    # Only check for minimum size, remove strict aspect ratio check
    if height < 240 or width < 320:  # minimum 240p
        print("Image resolution too low. Minimum 320x240 required.")
        return False
    
    return True

def frame_count_and_save(cap):
    frames = []
    frame_skip = 8
    frame_index = 1
    max_frames = 10
    
    while True:
        status, frame = cap.read()
        if not status:
            break
            
        if frame_index % frame_skip == 0:
            # Resize and convert to grayscale immediately to save memory
            target_height = 640
            aspect_ratio = frame.shape[1] / frame.shape[0]
            target_width = int(target_height * aspect_ratio)
            
            if target_width > 1280:
                target_width = 1280
                target_height = int(target_width / aspect_ratio)
                
            frame = cv2.resize(frame, (target_width, target_height))
            frames.append(frame)
            
            # Keep only required frames
            if len(frames) > max_frames:
                frames.pop(0)
            
        frame_index += 1
        
        # Force cleanup every 50 frames
        if frame_index % 50 == 0:
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
    cap.release()
    return frames

def process_frame(frame, image_cropper):
    prediction = None
    img = None
    try:
        if frame is None or not check_image(frame):
            logger.warning("Invalid frame or failed image check")
            return None
            
        logger.info("Starting face detection...")
        bbox = get_bbox(frame)
        if not bbox:
            logger.warning("No face detected in frame")
            return "SPOOF"
        logger.info(f"Face detected with bbox: {bbox}")
            
        prediction = np.zeros((1, 3))
        valid_predictions = 0
        
        logger.info(f"Processing with models: {list(_models.keys())}")
        if not _models:
            logger.error("No models loaded in _models dictionary!")
            return "SPOOF"
            
        for model_name, model in _models.items():
            try:
                logger.info(f"Processing with model: {model_name}")
                h_input, w_input, model_type, scale = parse_model_name(model_name)
                param = {
                    "org_img": frame,
                    "bbox": bbox,
                    "scale": scale,
                    "out_w": w_input,
                    "out_h": h_input,
                    "crop": True if scale is not None else False,
                }
                
                logger.info(f"Model parameters: {param}")
                
                # Process in smaller chunks with proper cleanup
                with torch.no_grad():
                    try:
                        logger.info("Attempting to crop image...")
                        img = image_cropper.crop(**param)
                        if img is None:
                            logger.warning(f"Failed to crop image for model {model_name}")
                            continue
                        logger.info(f"Successfully cropped image for model {model_name}")
                            
                        logger.info("Running prediction...")
                        pred = predict(img, model)
                        logger.info(f"Raw prediction output: {pred}")
                        
                        if pred is not None and pred.any():
                            prediction += pred
                            valid_predictions += 1
                            logger.info(f"Valid prediction from model {model_name}: {pred}")
                        else:
                            logger.warning(f"Model {model_name} returned empty prediction: {pred}")
                            
                    except Exception as e:
                        logger.error(f"Error processing with model {model_name}: {str(e)}", exc_info=True)
                        continue
                        
                    finally:
                        # Immediate cleanup of temporary tensors
                        if img is not None:
                            del img
                            img = None
                        if torch.cuda.is_available():
                            torch.cuda.empty_cache()
                            if hasattr(torch.cuda, 'ipc_collect'):
                                torch.cuda.ipc_collect()
                        gc.collect()
                        
            except Exception as e:
                logger.error(f"Error in model processing loop for {model_name}: {str(e)}", exc_info=True)
                continue
                
        if prediction is None or not prediction.any() or valid_predictions == 0:
            logger.warning(f"No valid prediction generated. Valid predictions: {valid_predictions}, Prediction array: {prediction}")
            return "SPOOF"
            
        # Average the predictions
        if valid_predictions > 0:
            prediction = prediction / valid_predictions
            
        label = np.argmax(prediction)
        value = prediction[0][label] / 2
        
        logger.info(f"Final prediction - Label: {label}, Value: {value}, Valid predictions: {valid_predictions}, Raw prediction: {prediction}")
        result = "LIVE" if (label == 1 and value > 0.55) or (label == 2 and value < 0.45) else "SPOOF"
        print(f"--------------------Result: {result} Label: {label} and Value: {value}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in process_frame: {str(e)}", exc_info=True)
        return "SPOOF"
        
    finally:
        # Ensure all resources are cleaned up
        try:
            if prediction is not None:
                del prediction
            if img is not None:
                del img
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except Exception as e:
            logger.error(f"Error in process_frame cleanup: {str(e)}", exc_info=True)

def liveness_worker(video_path, result_queue):
    """Worker function that runs in isolated process with its own memory space"""
    try:
        import gc
        import torch
        import cv2
        import logging
        import os
        from idvpackage.spoof_resources.generate_patches import CropImage
        import pkg_resources
        
        
        try:
            # Initialize models
            _models = {}
            model_paths = {
                '2.7_80x80_MiniFASNetV2.pth': pkg_resources.resource_filename('idvpackage', 'spoof_resources/2.7_80x80_MiniFASNetV2.pth'),
                '4_0_0_80x80_MiniFASNetV1SE.pth': pkg_resources.resource_filename('idvpackage', 'spoof_resources/4_0_0_80x80_MiniFASNetV1SE.pth')
            }
            
            _image_cropper = CropImage()
            
            # Load models
            for model_name, model_path in model_paths.items():
                if os.path.exists(model_path):
                    _models[model_name] = load_model(model_path)
                    gc.collect()
            
            # Process video
            cap = cv2.VideoCapture(video_path)
            frames = frame_count_and_save(cap)
            cap.release()
            
            if len(frames) < 3:
                result_queue.put('consider')
                return
            
            # Select frames to process
            if len(frames) > 6:
                indices = [0, 3, 6, -7, -4, -1]
                frames_to_process = [frames[i] for i in indices if -len(frames) <= i < len(frames)]
            else:
                frames_to_process = frames[:]
            
            del frames
            gc.collect()
            
            # Process frames
            all_predictions = []
            batch_size = 2
            
            for i in range(0, len(frames_to_process), batch_size):
                batch = frames_to_process[i:i + batch_size]
                
                for frame in batch:
                    if frame is not None:
                        result = process_frame(frame, _image_cropper)
                        if result:
                            all_predictions.append(result)
                    
                    del frame
                    gc.collect()
                
                del batch
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
            
            del frames_to_process
            gc.collect()
            
            if not all_predictions:
                result_queue.put('consider')
                return
            
            # Calculate result
            spoof_count = all_predictions.count('SPOOF')
            total_frames = len(all_predictions)
            result = 'consider' if spoof_count / total_frames >= 0.4 else 'clear'
            
            result_queue.put(result)
            
        except Exception as e:
            logging.error(f"Error in liveness worker: {e}")
            result_queue.put('consider')
            
        finally:
            # Cleanup
            try:
                if '_models' in locals():
                    for model in _models.values():
                        if hasattr(model, 'cpu'):
                            model.cpu()
                        del model
                    _models.clear()
                
                if '_image_cropper' in locals():
                    del _image_cropper
                
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                    if hasattr(torch.cuda, 'ipc_collect'):
                        torch.cuda.ipc_collect()
                
                gc.collect()
                
            except Exception as e:
                logging.error(f"Error in worker cleanup: {e}")
                
    except Exception as e:
        logging.error(f"Critical error in liveness worker: {e}")
        result_queue.put('consider')

def test(video_path):
    """Main function to handle worker process with timeout"""
    try:
        # Create queue for result communication
        result_queue = multiprocessing.Queue()
        
        # Create and start worker process
        process = multiprocessing.Process(
            target=liveness_worker,
            args=(video_path, result_queue),
            daemon=True
        )
        
        process.start()
        process.join(timeout=60)  # 60 second timeout for video processing
        
        # Check if process completed successfully
        if process.is_alive():
            logging.error("Liveness detection process timed out")
            process.terminate()
            process.join()
            return 'consider'
        
        # Get results if available
        if not result_queue.empty():
            result = result_queue.get()
            logging.info(f"Liveness detection completed. Result: {result}")
            return result
        
        logging.warning("No results returned from liveness detection process")
        return 'consider'
        
    except Exception as e:
        logging.error(f"Error in liveness detection controller: {e}")
        return 'consider'
    finally:
        # Ensure process is cleaned up
        if 'process' in locals() and process.is_alive():
            process.terminate()
            process.join()
        
        # Clear queue
        if 'result_queue' in locals():
            while not result_queue.empty():
                result_queue.get()

