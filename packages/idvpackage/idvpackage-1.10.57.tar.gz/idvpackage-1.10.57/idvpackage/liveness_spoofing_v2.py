import os
import sys
import logging

# Initialize PyTorch with error handling
try:
    import torch
    import torch.nn as nn
    if not hasattr(torch, '_C'):
        raise ImportError("PyTorch C++ extension (_C) not found. Try reinstalling PyTorch")
except ImportError as e:
    logging.error(f"Failed to initialize PyTorch: {e}")
    raise

import cv2
import os
import numpy as np
from deepface import DeepFace
from idvpackage.spoof_resources.generate_patches import CropImage
import torch.nn.functional as F
from idvpackage.spoof_resources.MiniFASNet import MiniFASNetV1SE, MiniFASNetV2
from idvpackage.spoof_resources import transform as trans
import pkg_resources
from concurrent.futures import ThreadPoolExecutor
import gc
import torch.cuda
import psutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_MAPPING = {
    'MiniFASNetV1SE': MiniFASNetV1SE,
    'MiniFASNetV2': MiniFASNetV2
}

# Global variables for model caching
_models = {}
_image_cropper = None
_device = 'cpu'

def log_memory_usage():
    """Log current process memory usage"""
    process = psutil.Process()
    logger.info(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")

def cleanup_models():
    """Clean up cached models and free memory"""
    global _models, _image_cropper
    if _models:
        for model_name in list(_models.keys()):
            try:
                model = _models[model_name]
                del model
                del _models[model_name]
            except:
                pass
        _models.clear()
        _models = {}
    
    if _image_cropper:
        del _image_cropper
        _image_cropper = None
    
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

def _initialize_resources():
    global _models, _image_cropper, _device
    if not _models:
        cleanup_models()  # Ensure clean state
        gc.collect()
        torch.cuda.empty_cache() if torch.cuda.is_available() else None
        
        _models = {
            '2.7_80x80_MiniFASNetV2.pth': load_model(pkg_resources.resource_filename('idvpackage', 'spoof_resources/2.7_80x80_MiniFASNetV2.pth')),
            '4_0_0_80x80_MiniFASNetV1SE.pth': load_model(pkg_resources.resource_filename('idvpackage', 'spoof_resources/4_0_0_80x80_MiniFASNetV1SE.pth'))
        }
    if not _image_cropper:
        _image_cropper = CropImage()

def get_bbox(frame):
    try:
        face_objs = DeepFace.extract_faces(frame, detector_backend='fastmtcnn')
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
            
        bbox = get_bbox(frame)
        if not bbox:
            logger.warning("No face detected in frame")
            return "SPOOF"
            
        prediction = np.zeros((1, 3))
        
        for model_name, model in _models.items():
            try:
                h_input, w_input, model_type, scale = parse_model_name(model_name)
                param = {
                    "org_img": frame,
                    "bbox": bbox,
                    "scale": scale,
                    "out_w": w_input,
                    "out_h": h_input,
                    "crop": True if scale is not None else False,
                }
                
                # Process in smaller chunks with proper cleanup
                with torch.no_grad():
                    try:
                        img = image_cropper.crop(**param)
                        if img is None:
                            logger.warning(f"Failed to crop image for model {model_name}")
                            continue
                            
                        pred = predict(img, model)
                        prediction += pred
                        
                    except Exception as e:
                        logger.error(f"Error processing with model {model_name}: {e}")
                        continue
                        
                    finally:
                        # Immediate cleanup of temporary tensors
                        if img is not None:
                            del img
                            img = None
                        torch.cuda.empty_cache() if torch.cuda.is_available() else None
                        gc.collect()
                        
            except Exception as e:
                logger.error(f"Error in model processing loop: {e}")
                continue
                
        if prediction is None or not prediction.any():
            logger.warning("No valid prediction generated")
            return "SPOOF"
            
        label = np.argmax(prediction)
        value = prediction[0][label] / 2
        
        return "LIVE" if (label == 1 and value > 0.55) or (label == 2 and value < 0.45) else "SPOOF"
        
    except Exception as e:
        logger.error(f"Error in process_frame: {e}")
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
            logger.error(f"Error in process_frame cleanup: {e}")

def test(video_path):
    cap = None
    try:
        # log_memory_usage()  # Log initial memory
        
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return 'consider'
            
        _initialize_resources()
        
        # Initialize video capture with error handling
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                logger.error("Failed to open video capture")
                return 'consider'
        except Exception as e:
            logger.error(f"Error initializing video capture: {e}")
            return 'consider'
            
        frames = []
        try:
            frames = frame_count_and_save(cap)
        except Exception as e:
            logger.error(f"Error in frame extraction: {e}")
            return 'consider'
        finally:
            if cap is not None:
                cap.release()
        
        if len(frames) < 3:
            logger.warning("Insufficient frames extracted")
            return 'consider'
            
        # Only keep required frames and ensure they're in CPU memory
        frames_to_process = []
        try:
            if len(frames) > 6:
                indices = [0, 3, 6, -7, -4, -1]
                frames_to_process = [frames[i] for i in indices if -len(frames) <= i < len(frames)]
            else:
                frames_to_process = frames[:]
        except Exception as e:
            logger.error(f"Error in frame selection: {e}")
            return 'consider'
        finally:
            # Clear original frames from memory
            del frames
            gc.collect()
        
        all_predictions = []
        # Process frames in smaller batches with error handling
        batch_size = 2
        try:
            for i in range(0, len(frames_to_process), batch_size):
                batch = frames_to_process[i:i + batch_size]
                
                # Process each frame in the batch
                for frame in batch:
                    try:
                        if frame is None:
                            continue
                            
                        result = process_frame(frame, _image_cropper)
                        if result:
                            all_predictions.append(result)
                    except Exception as e:
                        logger.error(f"Error processing frame: {e}")
                        continue
                    finally:
                        # Ensure frame is released
                        del frame
                        
                # Cleanup after each batch
                del batch
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                    
            del frames_to_process
            gc.collect()
            
            if not all_predictions:
                logger.warning("No valid predictions generated")
                return 'consider'

            spoof_count = all_predictions.count('SPOOF')
            total_frames = len(all_predictions)
            
            result = 'consider' if spoof_count / total_frames >= 0.4 else 'clear'
            # log_memory_usage()  # Log final memory
            return result
            
        except Exception as e:
            logger.error(f"Error in prediction processing: {e}")
            return 'consider'
            
    except Exception as e:
        logger.error(f"Error in test function: {e}")
        return 'consider'
        
    finally:
        # Ensure all resources are properly cleaned up
        try:
            cleanup_models()  # Clean up models after processing
            if cap is not None:
                cap.release()
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except Exception as e:
            logger.error(f"Error in final cleanup: {e}")

