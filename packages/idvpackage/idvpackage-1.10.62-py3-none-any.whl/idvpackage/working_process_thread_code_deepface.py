## Working code
def process_image_worker(image_base64, result_queue):
    """Worker function that runs in isolated process with its own memory space"""
    try:
        # Import dependencies inside worker
        import gc
        import sys
        import torch
        import numpy as np
        import cv2
        import face_recognition
        import logging
        from PIL import Image
        import io
        from concurrent.futures import ThreadPoolExecutor, as_completed
        from deepface import DeepFace
        
        CONFIDENCE_THRESHOLD = 0.97
        
        def process_angle(image, angle):
            """Process image at a specific angle for face detection"""
            try:
                # Rotate image if needed
                if angle != 0:
                    if angle == 90:
                        rotated = cv2.rotate(image.copy(), cv2.ROTATE_90_CLOCKWISE)
                    elif angle == 180:
                        rotated = cv2.rotate(image.copy(), cv2.ROTATE_180)
                    elif angle == 270:
                        rotated = cv2.rotate(image.copy(), cv2.ROTATE_90_COUNTERCLOCKWISE)
                else:
                    rotated = image.copy()
                
                # Detect faces
                try:
                    face_objs = DeepFace.extract_faces(
                        img_path=rotated,
                        detector_backend='fastmtcnn',
                        enforce_detection=False,
                        align=True
                    )
                
                except Exception as e:
                    print(f"DeepFace.extract_faces error: {e}")
                confidence = face_objs[0].get('confidence', 0) if face_objs else 0
                logging.info(f"Processed angle {angle} with confidence {confidence}")
                
                return face_objs, rotated, confidence
                
            except Exception as e:
                logging.error(f"Error processing angle {angle}: {e}")
                return None, None, 0
            finally:
                if 'rotated' in locals() and angle != 0:
                    del rotated
                gc.collect()
        
        def extract_face_data(face_objs, processed_image):
            """Extract face locations and encodings from detected faces"""
            try:
                if not face_objs:
                    return None, None
                
                biggest_face = max(face_objs, key=lambda x: x['facial_area']['w'] * x['facial_area']['h'])
                area = biggest_face['facial_area']
                locations = [(area['y'], area['x'] + area['w'], area['y'] + area['h'], area['x'])]
                encodings = face_recognition.face_encodings(processed_image, locations)
                
                return (locations, encodings) if encodings else (None, None)
                
            except Exception as e:
                logging.error(f"Error extracting face data: {e}")
                return None, None
            finally:
                if 'biggest_face' in locals():
                    del biggest_face
                gc.collect()
        
        try:
            # Handle image conversion
            if isinstance(image_base64, bytes):
                image_data = image_base64
            else:
                image_data = base64.b64decode(image_base64)
            
            # Convert to PIL Image and then to numpy array
            with Image.open(io.BytesIO(image_data)) as image_pil:
                image_pil = image_pil.convert('RGB')
                image = np.array(image_pil)
            
            del image_data
            logging.info("Successfully loaded and converted image")
            
        except Exception as e:
            logging.error(f"Error in image conversion: {e}")
            result_queue.put(([], []))
            return
        
        try:
            # Try all angles in parallel
            angles = [0, 90, 180, 270]
            best_result = None
            best_confidence = 0
            
            with ThreadPoolExecutor(max_workers=4) as executor:
                # Submit all angles for processing
                future_to_angle = {
                    executor.submit(process_angle, image, angle): angle 
                    for angle in angles
                }
                
                # Process results as they complete
                for future in as_completed(future_to_angle):
                    angle = future_to_angle[future]
                    try:
                        face_objs, processed_image, confidence = future.result()
                        
                        if face_objs and confidence > best_confidence:
                            # Clean up previous best result
                            if best_result:
                                del best_result
                            
                            best_result = (face_objs, processed_image, confidence, angle)
                            best_confidence = confidence
                            
                            # If confidence is good enough, cancel remaining tasks
                            if confidence >= CONFIDENCE_THRESHOLD:
                                for f in future_to_angle:
                                    if not f.done():
                                        f.cancel()
                                break
                            
                    except Exception as e:
                        logging.error(f"Error processing angle {angle}: {e}")
                        continue
                    finally:
                        gc.collect()
            
            # Process best result
            if best_result:
                face_objs, processed_image, confidence, angle = best_result
                locations, encodings = extract_face_data(face_objs, processed_image)
                
                if locations and encodings:
                    logging.info(f"Best face found at angle {angle} with confidence {confidence}")
                    result_queue.put((locations, encodings))
                    return
            
            logging.warning("No valid faces found in any orientation")
            result_queue.put(([], []))
            
        except Exception as e:
            logging.error(f"Error in face detection/encoding: {e}")
            result_queue.put(([], []))
            
        finally:
            # Cleanup
            for var in ['image', 'best_result', 'face_objs', 'processed_image']:
                if var in locals():
                    del locals()[var]
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                
    except Exception as e:
        logging.error(f"Critical error in worker: {e}")
        result_queue.put(([], []))
    finally:
        gc.collect()

def load_and_process_image_deepface(image_base64):
    """Main function to handle worker process with timeout"""
    try:
        # Create queue for result communication
        result_queue = multiprocessing.Queue()
        
        # Create and start worker process
        process = multiprocessing.Process(
            target=process_image_worker,
            args=(image_base64, result_queue),
            daemon=True
        )
        
        # Start process with timeout
        process.start()
        process.join(timeout=30)  # 30 second timeout
        
        # Check if process completed successfully
        if process.is_alive():
            logging.error("Face detection process timed out")
            process.terminate()
            process.join()
            return [], []
        
        # Get results if available
        if not result_queue.empty():
            result = result_queue.get()
            logging.info(f"Face detection completed. Locations: {result[0]}")
            return result
            
        logging.warning("No results returned from face detection process")
        return [], []
        
    except Exception as e:
        logging.error(f"Error in face detection controller: {e}")
        return [], []
    finally:
        # Ensure process is cleaned up
        if 'process' in locals() and process.is_alive():
            process.terminate()
            process.join()
        
        # Clear queue
        if 'result_queue' in locals():
            while not result_queue.empty():
                result_queue.get()

