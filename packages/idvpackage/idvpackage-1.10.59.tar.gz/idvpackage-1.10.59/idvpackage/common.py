import os
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'  # Disable fork safety check
os.environ['NO_PROXY'] = 'localhost,127.0.0.1'  # Optional: Fixes some macOS socket issues

import re
from datetime import datetime
from itertools import permutations
import cv2
import numpy as np
from PIL import Image
import io
from google.cloud import vision_v1
import tempfile
import os
from io import BytesIO
import gc
import psutil
import logging
import functools
import sys
import torch
import base64
import multiprocessing
import platform

# multiprocessing.set_start_method('spawn', force=True)
print(f"Platform: {platform.system()}")

# if multiprocessing.current_process().name == 'MainProcess':
#     if platform.system() == 'Darwin':
#         multiprocessing.set_start_method('spawn', force=True)
#     else:
#         try:
#             multiprocessing.set_start_method('fork', force=True)
#         except ValueError:
#             multiprocessing.set_start_method('spawn', force=True)

# # Configure multiprocessing start method
# if platform.system() == 'Darwin':  # macOS
#     # Use 'spawn' on macOS to avoid issues with fork and Cocoa
#     multiprocessing.set_start_method('spawn', force=True)
# else:
try:
    # Try to use fork on other Unix systems
    multiprocessing.set_start_method('fork', force=True)
except ValueError:
    # Fall back to spawn if fork is not available
    multiprocessing.set_start_method('spawn', force=True)

def log_memory_usage(step):
    """Log current memory usage with step name"""
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024 / 1024
    logging.info(f"Memory usage at {step}: {memory_mb:.2f} MB")

# Lazy loading of heavy imports
_deepface = None
_face_recognition = None

def get_deepface():
    global _deepface
    if _deepface is None:
        from deepface import DeepFace
        _deepface = DeepFace
    return _deepface

def get_face_recognition():
    global _face_recognition
    if _face_recognition is None:
        import face_recognition
        _face_recognition = face_recognition
    return _face_recognition

# Global model cache
_model_cache = {}

def get_or_create_model(model_name, backend='fastmtcnn'):
    """Get model from cache or create new one"""
    global _model_cache
    
    cache_key = f"{model_name}_{backend}"
    if cache_key not in _model_cache:
        DeepFace = get_deepface()
        model = DeepFace.build_model(model_name)
        _model_cache[cache_key] = model
    return _model_cache[cache_key]

def clear_model_cache():
    """Clear the model cache and loaded modules"""
    global _model_cache, _deepface, _face_recognition
    
    # Clear model cache
    if _model_cache:
        for model in _model_cache.values():
            try:
                if hasattr(model, 'cpu'):
                    model.cpu()
                del model
            except:
                pass
        _model_cache.clear()
    
    # Clear loaded modules
    _deepface = None
    _face_recognition = None
    
    # Clear CUDA cache
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        if hasattr(torch.cuda, 'ipc_collect'):
            torch.cuda.ipc_collect()
        try:
            torch.cuda.memory.empty_cache()
            torch.cuda.memory._reset_memory_stats()
        except:
            pass
    
    # Multiple GC passes
    for _ in range(3):
        gc.collect()

def func_common_dates(  extract_no_space):
    dob = ''
    expiry_date = ''
    try:
        matches = re.findall(r'\d{2}/\d{2}/\d{4}', extract_no_space)
        y1 = matches[0][-4:]
        y2 = matches[1][-4:]
        if int(y1) < int(y2):
            dob = matches[0]
            expiry_date = matches[1]
        else:
            dob = matches[1]
            expiry_date = matches[0]
    except:
        dob = ''
        expiry_date = ''

    return dob, expiry_date

def convert_dob(input_date):
    day = input_date[4:6]
    month = input_date[2:4]
    year = input_date[0:2]

    current_year = datetime.now().year
    current_century = current_year // 100
    current_year_last_two_digits = current_year % 100

    century = current_century
    # If the given year is greater than the last two digits of the current year, assume last century
    if int(year) > current_year_last_two_digits:
        century = current_century - 1

    final_date = f"{day}/{month}/{century}{year}"

    return final_date

def func_dob(  extract):
    extract_no_space = extract.replace(' ','')
    dob, expiry_date = func_common_dates(extract_no_space)
    if dob == '':  
        match_dob = re.findall(r'\d{7}(?:M|F)\d', extract_no_space)
        for i in match_dob:
            # print(i)
            raw_dob = i[0:6]
            # print(raw_dob)
            year = str(datetime.today().year)[2:4]
            temp = '19'
            if int(raw_dob[0:2]) > int(year):
                temp = '19'
            else:
                temp = '20'      
            dob = raw_dob[4:6]+'/'+raw_dob[2:4]+'/'+temp+raw_dob[0:2]
            try:
                dt_obj = datetime.strptime(dob, '%d/%m/%Y')
                break
            except:
                # print(f'invalid date {dob}')
                dob = ''
        else:
            pattern = r"\b(\d{14}).*?\b"

            new_dob_match = re.search(pattern, extract_no_space)

            if new_dob_match:
                new_dob = new_dob_match.group(1)
                new_dob = new_dob[:7]
                dob = convert_dob(new_dob)

    return dob

def func_expiry_date(  extract):
    extract_no_space = extract.replace(' ','')
    dob, expiry_date = func_common_dates(extract_no_space)
    if expiry_date == '':
        match_doe = re.findall(r'\d{7}[A-Z]{2,3}', extract_no_space) 
        for i in match_doe:
         
            raw_doe = i[0:6]
            # print(raw_doe)
            expiry_date = raw_doe[4:6]+'/'+raw_doe[2:4]+'/20'+raw_doe[0:2]
            try:
                dt_obj = datetime.strptime(expiry_date, '%d/%m/%Y')
                break
            except:
   
                expiry_date = ''

    return expiry_date

def convert_expiry_date(input_date):
    day = input_date[4:6]
    month = input_date[2:4]
    year = input_date[0:2]

    current_year = datetime.now().year
    current_century = current_year // 100
    current_year_last_two_digits = current_year % 100
    century = current_century

    if int(year) <= current_year_last_two_digits:
        century = current_century
    else:
        century = current_century
    final_date = f"{day}/{month}/{century}{year}"

    return final_date

def extract_first_9_digits(string_input):
    match = re.search(r'\b\d{9}\b', string_input)
    if match:
        sequence = match.group(0)
        return sequence
    else:
        return ""

def func_card_number(  extract):
    extract_no_space = extract.replace(' ','')
    try:
        card_number = re.search(r'\d{9}', extract_no_space).group()
    except:
        card_number=  extract_first_9_digits(extract_no_space)

    return card_number


def count_digits_after_pattern(s):
    """
    Counts the number of digits that come after a specified pattern in a string.

    Parameters:
    s (str): The input string.
    pattern (str): The pattern to search for.

    Returns:
    int: The count of digits that come after the pattern.
    """
    # Construct the regex pattern to find the specified pattern followed by digits
    pattern = "<<<<"
    regex_pattern = re.compile(f"{re.escape(pattern)}(\d+)")
    
    # Search for the pattern in the string
    match = regex_pattern.search(s)
    
    # If a match is found, count the digits
    if match:
        digits_after_pattern = match.group(1)
        return len(digits_after_pattern)
    else:
        return 0  # Pattern not found

def remove_special_characters1(string):
    # This pattern matches any character that is not a letter, digit, or space
    #pattern = r'[^a-zA-Z0-9<\s]'
    pattern = r'[^a-zA-Z0-9<>]'
    return re.sub(pattern, '', string)

def remove_special_characters_mrz2(string):
    # This pattern matches any character that is not a letter, digit, or space
    pattern = r'[^a-zA-Z0-9\s]'
    return re.sub(pattern, '', string)

def validate_string(s):
    """
    Validates if the string follows the specific structure.

    Structure: 7 digits, followed by 'M' or 'F', then 7 digits again,
    then 3 uppercase letters, and ending with 1 digit.

    Parameters:
    s (str): The string to be validated.

    Returns:
    bool: True if the string follows the structure, False otherwise.
    """
    pattern = r'^\d{7}[MF]\d{7}[A-Z]{3}\d$'
    return bool(re.match(pattern, s))


def remove_special_characters2(string):
    # This pattern matches any character that is not a letter, digit, or space
    pattern = r'[^a-zA-Z0-9\s]'
    return re.sub(pattern, ' ', string)

def func_name(extract):
    bio_data = extract[-40:]
    breakup = bio_data.split('\n')
    if len(breakup) == 2:
        name_extract = breakup.pop(0)
    else:
        country_extract = breakup.pop(0).replace(" ","")
        name_extract = breakup.pop(0)

# Check the alphanumeric nature of name_extract
    if not name_extract.isupper():
        name_extract = breakup.pop(0)
    
    try:
        name = name_extract.replace("<", " ").replace(">", " ").replace(".", " ").replace(":", " ").replace('«','').strip()
        name = ' '.join(name.split())
        name = name.replace("0", "O") # special case fix
    except:
        name = ""

    return name

def func_nationality(  extract):
    extract_no_space = extract.replace(' ','')
    try:
        pattern = r'\d{5}[A-Z]{3}|\d{5}[A-Z]{2}'

        m = re.findall(pattern, extract_no_space)
        country = m[len(m)-1].replace("<", "")[5:]
    except:
        country = ""

    if country == '':
        try:
            pattern = r'\d{2}[a-z][A-Z]{2}'

            m = re.findall(pattern, extract_no_space)
            country = m[len(m)-1].replace("<", "")[2:].upper()
        except:
            country = ""

    return country

def clean_string(input_string):
        cleaned_string = re.sub(r'[^\w\s]', ' ', input_string)
        return cleaned_string.strip()

def count_digits(element):
    digits = [char for char in element if char.isdigit()]
    return len(digits)
    
def find_and_slice_number(input_number, digits):
    # Generate all possible permutations of the digits
    perms = [''.join(p) for p in permutations(digits)]
    
    # Initialize variables to keep track of the found pattern and its index
    found_pattern = None
    found_index = -1

    # Search for any permutation of the digits in the input_number
    for perm in perms:
        found_index = input_number.find(perm)
        if found_index != -1:
            found_pattern = perm
            break

    # If a pattern is found, slice the number accordingly
    if found_pattern:
        if found_index > len(input_number) - found_index - len(found_pattern):
            # Slice to the left
            sliced_number = input_number[:found_index + len(found_pattern)]
        else:
            # Slice to the right
            sliced_number = input_number[found_index:]
        
        return sliced_number
    else:
        return ''
    
def func_id_number(extract,dob):
        
    try:
        p = "784" + "\d{12}"
        id_re = re.search(p, clean_string(extract).replace(' ',''))
        id_number = id_re.group()
    except:
        
        try:
            pattern = r'\d{15,}'
            digits = '784'
            matches = re.findall(pattern, clean_string(extract).replace(' ',''))
            input_number = matches[0]
            dob=dob[-4:]
            id_number='784'+dob+find_and_slice_number(input_number, digits)[:8]
            
        except:
            id_number = ''

    return id_number


# #year = dob[-4:]
# p = "784" + "\d{12}"
# id_re = re.search(p, clean_string(data).replace(' ',''))
# id_number = id_re.group()



def convert_to_date(date_str):
    year = '19' + date_str[:2] if int(date_str[:2]) >= 50 else '20' + date_str[:2]
    month = date_str[2:4]
    day = date_str[4:6]
    return f"{day}/{month}/{year}"

def check_valid_date(date_str, format="%d/%m/%Y"):
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False
    

def find_expiry_date(original_text,mrz2):
    
    dates = re.findall(r'\b\d{2}/\d{2}/\d{4}\b', original_text)
    expiry_date = ''

    if len(dates) == 2:
        
        date1 = datetime.strptime(dates[0], '%d/%m/%Y')
        date2 = datetime.strptime(dates[1], '%d/%m/%Y')
        
        if date2 < date1:
            expiry_date = dates[0]
        elif date2 > date1:
            expiry_date = dates[1]
            
    elif mrz2:
        match_expiry_date = re.search(r'[A-Za-z](\d+)', mrz2)
        if match_expiry_date:
            expiry_date = match_expiry_date.group(1)[:6]
            expiry_date = convert_to_date(expiry_date)
    
            
    if not check_valid_date(expiry_date):
            expiry_date=''
    return expiry_date

def find_dob(original_text,mrz2):
    
     dates = re.findall(r'\b\d{2}/\d{2}/\d{4}\b', original_text)
     dob = ''
  
     if len(dates) == 2:
            date1 = datetime.strptime(dates[0], '%d/%m/%Y')
            date2 = datetime.strptime(dates[1], '%d/%m/%Y')

            if date2 < date1:
                dob = dates[1]
            elif date2 > date1:
                dob = dates[0] 
                
     elif mrz2:
        match_dob = re.search(r'(\d+)[A-Za-z]', mrz2)
        if match_dob:
            dob = match_dob.group(1)[:6] 
            dob=convert_to_date(dob)
    
     if not check_valid_date(dob):
            dob=''
     return dob


def convert_date_format(date_str):
    # Parse the date from DD/MM/YYYY format
    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
    # Convert it to YYYY-MM-DD format
    formatted_date = date_obj.strftime('%Y-%m-%d')
    return formatted_date


def convert_gender(gender_char):
    if gender_char.lower() == 'm':
        return 'Male'
    elif gender_char.lower() == 'f': 
        return 'Female'
    else:  
        return ''


def compute_ela_cv(orig_img, quality):
    SCALE = 15
    orig_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2RGB)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        temp_filename = temp_file.name

        cv2.imwrite(temp_filename, orig_img, [cv2.IMWRITE_JPEG_QUALITY, quality])
        # read compressed image
        compressed_img = cv2.imread(temp_filename)

        # get absolute difference between img1 and img2 and multiply by scale
        diff = SCALE * cv2.absdiff(orig_img, compressed_img)
    
    # delete the temporary file
    if os.path.exists(temp_filename):
        os.remove(temp_filename)

    return diff


def calculate_error_difference(orig_img, country=None):
    if isinstance(orig_img, Image.Image):
        orig_img = np.array(orig_img)
        
    if np.any(orig_img):
        ela_val = compute_ela_cv(orig_img, quality=94)
        diff_avg = ela_val.mean()

        print(f"DIFFERENCE: {diff_avg}")
        if country == 'UAE':
            if diff_avg <= 25:
                label = 'Genuine'
            else:
                label = 'Tampered'
        else:
            if diff_avg <= 10.5:
                label = 'Genuine'
            else:
                label = 'Tampered'
                
        return label
    else:
        print(f"ISSUE")
        return 'Genuine'


def eastern_arabic_to_english(eastern_numeral):
    try:
        arabic_to_english_map = {
            '٠': '0', '۰': '0',
            '١': '1', '۱': '1',
            '٢': '2', '۲': '2',
            '٣': '3', '۳': '3',
            '٤': '4', '۴': '4',
            '٥': '5', '۵': '5',
            '٦': '6', '۶': '6',
            '٧': '7', '۷': '7',
            '٨': '8', '۸': '8',
            '٩': '9', '۹': '9',
            '/': '/'
        }

        english_numeral = ''.join([arabic_to_english_map[char] if char in arabic_to_english_map else char for char in eastern_numeral])
        
        return english_numeral

    except:
        return eastern_numeral

def english_to_eastern_arabic(english_numeral):
    try:
        english_to_arabic_map = {
            '0': '٠', 
            '1': '١', 
            '2': '٢', 
            '3': '٣', 
            '4': '٤', 
            '5': '٥', 
            '6': '٦', 
            '7': '٧', 
            '8': '٨', 
            '9': '٩'
        }

        eastern_arabic_numeral = ''.join([english_to_arabic_map[char] if char in english_to_arabic_map else char for char in english_numeral])
        
        return eastern_arabic_numeral

    except Exception as e:
        return str(e)  

def crop_third_part(img):
    width, height = img.size
    part_height = height // 3
    third_part = img.crop((0, 2 * part_height, width, height))
    # third_part.save("/Users/fahadpatel/Pictures/thirdpart.jpg")
    return third_part

def extract_text_from_image_data(client, image):
    """Detects text in the file."""

    # with io.BytesIO() as output:
    #     image.save(output, format="PNG")
    #     content = output.getvalue()

    compressed_image = BytesIO()
    image.save(compressed_image, format="JPEG", quality=100, optimize=True)
    content = compressed_image.getvalue()

    image = vision_v1.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    return texts[0].description

def detect_id_card_uae(client, image_data, id_text, part=None):
    if id_text:
        vertices = id_text[0].bounding_poly.vertices
        left = vertices[0].x
        top = vertices[0].y
        right = vertices[2].x
        bottom = vertices[2].y

        padding = 30
        left -= padding
        top -= padding
        right += padding
        bottom += padding

        # img = image_data

        with Image.open(io.BytesIO(image_data)) as img:
            id_card = img.crop((max(0, left), max(0, top), right, bottom))
            width, height = id_card.size
            if width < height:
                id_card = id_card.rotate(90, expand=True)
            
            tampered_result = calculate_error_difference(id_card, country = 'UAE')

            part_text = id_text[0].description
            if part == 'third':
                part_img = crop_third_part(id_card)
                part_text = extract_text_from_image_data(client, part_img)

            return  tampered_result, part_text

def rotate_image(img):
        from skimage.transform import radon
        
        img_array = np.array(img)

        if len(img_array.shape) == 2:
            gray = img_array
        else:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        h, w = gray.shape
        if w > 640:
            gray = cv2.resize(gray, (640, int((h / w) * 640)))
        gray = gray - np.mean(gray)
        sinogram = radon(gray)
        r = np.array([np.sqrt(np.mean(np.abs(line) ** 2)) for line in sinogram.transpose()])
        rotation = np.argmax(r)
        angle = round(abs(90 - rotation) + 0.5)

        if abs(angle) > 5:
            rotated_img = img.rotate(angle, expand=True)
            return rotated_img

        return img

def aggressive_cleanup():
    """Aggressively clean up memory"""
    # Clear model cache
    clear_model_cache()
    
    # Clear any loaded ML modules
    modules_to_clear = [
        'deepface', 'face_recognition', 'tensorflow', 
        'torch', 'torchvision', 'PIL', 'cv2'
    ]
    
    for module in modules_to_clear:
        if module in sys.modules:
            try:
                del sys.modules[module]
            except:
                pass
    
    # Clear any remaining tensors
    if torch.cuda.is_available():
        try:
            # Clear CUDA cache
            torch.cuda.empty_cache()
            if hasattr(torch.cuda, 'ipc_collect'):
                torch.cuda.ipc_collect()
            
            # Reset memory stats
            torch.cuda.memory.empty_cache()
            torch.cuda.memory._reset_memory_stats()
            
            # Clear any remaining tensors
            for obj in gc.get_objects():
                try:
                    if torch.is_tensor(obj):
                        obj.detach_()
                        del obj
                except:
                    pass
        except Exception as e:
            logging.warning(f"PyTorch cleanup failed: {e}")
    
    # Multiple garbage collection passes
    for _ in range(3):
        gc.collect()
        
    # Clear any remaining large objects
    for obj in gc.get_objects():
        try:
            if sys.getsizeof(obj) > 1024 * 1024:  # Objects larger than 1MB
                del obj
        except:
            pass
    
    gc.collect()


## Initial code
# def load_and_process_image_deepface(image_base64):
#         import base64
#         from deepface import DeepFace
#         import face_recognition

#         face_locations, face_encodings, face_objs = [], [], []

#         image_data = base64.b64decode(image_base64)
#         image_np = np.frombuffer(image_data, np.uint8)
#         image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

#         try:
#             face_objs = DeepFace.extract_faces(image, detector_backend = 'fastmtcnn')
#             # print(f'FACE_OBJ 1: {face_objs}')
#             confidence = face_objs[0].get('confidence', 0)
#             # print(f'\n\nConfidence: {confidence}\n\n')

#             if confidence < 0.97:
#                 image = cv2.rotate(image, cv2.ROTATE_180)
#                 face_objs = DeepFace.extract_faces(image, detector_backend = 'fastmtcnn')
#         except:
#             image_pil_orig = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#             try:
#                 image_pil = rotate_image(image_pil_orig)
#                 image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

#                 face_objs = DeepFace.extract_faces(image, detector_backend = 'fastmtcnn')
#                 # print(f'FACE_OBJ 2: {face_objs}')

#                 confidence = face_objs[0].get('confidence', 0)
#                 # print(f'\n\nConfidence 2: {confidence}\n\n')
#                 if confidence < 0.97:
#                     image = cv2.rotate(image, cv2.ROTATE_180)
#                     face_objs = DeepFace.extract_faces(image, detector_backend = 'fastmtcnn')
#                     # print(f'FACE_OBJ 3: {face_objs}')
#             except:
#                 try:
#                     image_pil = image_pil.rotate(180, expand=True)
#                     image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

#                     face_objs = DeepFace.extract_faces(image, detector_backend = 'fastmtcnn')
#                     # print(f'FACE_OBJ 4: {face_objs}')
#                 except:
#                     print(f'Unable to extract face from ID')
#                     face_objs = []
                
#         if face_objs:
#             biggest_face = max(face_objs, key=lambda face: face['facial_area']['w'] * face['facial_area']['h'])
#             facial_area = biggest_face['facial_area']
#             x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']

#             face_locations = [(y, x + w, y + h, x)]
#             face_encodings = face_recognition.face_encodings(image, face_locations)

#         return face_locations, face_encodings



## Working code
# def process_image_worker(image_base64, result_queue):
#     """Worker function that runs in isolated process with its own memory space"""
#     try:
#         # Import dependencies inside worker
#         import gc
#         import sys
#         import torch
#         import numpy as np
#         import cv2
#         import face_recognition
#         import logging
#         from PIL import Image
#         import io
#         from concurrent.futures import ThreadPoolExecutor, as_completed
#         from deepface import DeepFace
        
#         CONFIDENCE_THRESHOLD = 0.97
        
#         def process_angle(image, angle):
#             """Process image at a specific angle for face detection"""
#             try:
#                 # Rotate image if needed
#                 if angle != 0:
#                     if angle == 90:
#                         rotated = cv2.rotate(image.copy(), cv2.ROTATE_90_CLOCKWISE)
#                     elif angle == 180:
#                         rotated = cv2.rotate(image.copy(), cv2.ROTATE_180)
#                     elif angle == 270:
#                         rotated = cv2.rotate(image.copy(), cv2.ROTATE_90_COUNTERCLOCKWISE)
#                 else:
#                     rotated = image.copy()
                
#                 # Detect faces
#                 try:
#                     face_objs = DeepFace.extract_faces(
#                         img_path=rotated,
#                         detector_backend='mtcnn',
#                         enforce_detection=False,
#                         align=True
#                     )
                
#                 except Exception as e:
#                     print(f"DeepFace.extract_faces error: {e}")
#                 confidence = face_objs[0].get('confidence', 0) if face_objs else 0
#                 logging.info(f"Processed angle {angle} with confidence {confidence}")
                
#                 return face_objs, rotated, confidence
                
#             except Exception as e:
#                 logging.error(f"Error processing angle {angle}: {e}")
#                 return None, None, 0
#             finally:
#                 if 'rotated' in locals() and angle != 0:
#                     del rotated
#                 gc.collect()
        
#         def extract_face_data(face_objs, processed_image):
#             """Extract face locations and encodings from detected faces"""
#             try:
#                 if not face_objs:
#                     return None, None
                
#                 biggest_face = max(face_objs, key=lambda x: x['facial_area']['w'] * x['facial_area']['h'])
#                 area = biggest_face['facial_area']
#                 locations = [(area['y'], area['x'] + area['w'], area['y'] + area['h'], area['x'])]
#                 encodings = face_recognition.face_encodings(processed_image, locations)
                
#                 return (locations, encodings) if encodings else (None, None)
                
#             except Exception as e:
#                 logging.error(f"Error extracting face data: {e}")
#                 return None, None
#             finally:
#                 if 'biggest_face' in locals():
#                     del biggest_face
#                 gc.collect()
        
#         try:
#             # Handle image conversion
#             if isinstance(image_base64, bytes):
#                 image_data = image_base64
#             else:
#                 image_data = base64.b64decode(image_base64)
            
#             # Convert to PIL Image and then to numpy array
#             with Image.open(io.BytesIO(image_data)) as image_pil:
#                 image_pil = image_pil.convert('RGB')
#                 image = np.array(image_pil)
            
#             del image_data
#             logging.info("Successfully loaded and converted image")
            
#         except Exception as e:
#             logging.error(f"Error in image conversion: {e}")
#             result_queue.put(([], []))
#             return
        
#         try:
#             # Try all angles in parallel
#             angles = [0, 90, 180, 270]
#             best_result = None
#             best_confidence = 0
            
#             with ThreadPoolExecutor(max_workers=4) as executor:
#                 # Submit all angles for processing
#                 future_to_angle = {
#                     executor.submit(process_angle, image, angle): angle 
#                     for angle in angles
#                 }
                
#                 # Process results as they complete
#                 for future in as_completed(future_to_angle):
#                     angle = future_to_angle[future]
#                     try:
#                         face_objs, processed_image, confidence = future.result()
                        
#                         if face_objs and confidence > best_confidence:
#                             # Clean up previous best result
#                             if best_result:
#                                 del best_result
                            
#                             best_result = (face_objs, processed_image, confidence, angle)
#                             best_confidence = confidence
                            
#                             # If confidence is good enough, cancel remaining tasks
#                             if confidence >= CONFIDENCE_THRESHOLD:
#                                 for f in future_to_angle:
#                                     if not f.done():
#                                         f.cancel()
#                                 break
                            
#                     except Exception as e:
#                         logging.error(f"Error processing angle {angle}: {e}")
#                         continue
#                     finally:
#                         gc.collect()
            
#             # Process best result
#             if best_result:
#                 face_objs, processed_image, confidence, angle = best_result
#                 locations, encodings = extract_face_data(face_objs, processed_image)
                
#                 if locations and encodings:
#                     logging.info(f"Best face found at angle {angle} with confidence {confidence}")
#                     result_queue.put((locations, encodings))
#                     return
            
#             logging.warning("No valid faces found in any orientation")
#             result_queue.put(([], []))
            
#         except Exception as e:
#             logging.error(f"Error in face detection/encoding: {e}")
#             result_queue.put(([], []))
            
#         finally:
#             # Cleanup
#             for var in ['image', 'best_result', 'face_objs', 'processed_image']:
#                 if var in locals():
#                     del locals()[var]
#             gc.collect()
#             if torch.cuda.is_available():
#                 torch.cuda.empty_cache()
                
#     except Exception as e:
#         logging.error(f"Critical error in worker: {e}")
#         result_queue.put(([], []))
#     finally:
#         gc.collect()

# def load_and_process_image_deepface(image_base64):
#     """Main function to handle worker process with timeout"""
#     try:
#         # Create queue for result communication
#         result_queue = multiprocessing.Queue()
        
#         # Create and start worker process
#         process = multiprocessing.Process(
#             target=process_image_worker,
#             args=(image_base64, result_queue),
#             daemon=True
#         )
        
#         # Start process with timeout
#         process.start()
#         process.join(timeout=30)  # 30 second timeout
        
#         # Check if process completed successfully
#         if process.is_alive():
#             logging.error("Face detection process timed out")
#             process.terminate()
#             process.join()
#             return [], []
        
#         # Get results if available
#         if not result_queue.empty():
#             result = result_queue.get()
#             logging.info(f"Face detection completed. Locations: {result[0]}")
#             return result
            
#         logging.warning("No results returned from face detection process")
#         return [], []
        
#     except Exception as e:
#         logging.error(f"Error in face detection controller: {e}")
#         return [], []
#     finally:
#         # Ensure process is cleaned up
#         if 'process' in locals() and process.is_alive():
#             process.terminate()
#             process.join()
        
#         # Clear queue
#         if 'result_queue' in locals():
#             while not result_queue.empty():
#                 result_queue.get()

def process_image_worker(image_base64, result_queue):
    """Worker process optimized for macOS stability"""
    try:
        # Isolate heavy imports INSIDE the worker
        import cv2
        import numpy as np
        from PIL import Image
        import io
        import logging
        from deepface import DeepFace

        # Lightweight face recognition (avoid if possible)
        import face_recognition  

        # --- Image Loading ---
        try:
            if isinstance(image_base64, bytes):
                image_data = image_base64
            else:
                image_data = base64.b64decode(image_base64)
            
            with Image.open(io.BytesIO(image_data)) as img:
                image = np.array(img.convert("RGB"))
            del image_data
        except Exception as e:
            logging.error(f"Image load failed: {e}")
            result_queue.put(([], []))
            return

        # --- Face Detection Logic ---
        best_face = None
        for angle in [0, 90, 180, 270]:
            try:
                # Rotate image
                if angle == 0:
                    rotated = image.copy()
                else:
                    rotated = cv2.rotate(image, {
                        90: cv2.ROTATE_90_CLOCKWISE,
                        180: cv2.ROTATE_180,
                        270: cv2.ROTATE_90_COUNTERCLOCKWISE
                    }[angle])
                
                # Detect with DeepFace
                faces = DeepFace.extract_faces(
                    img_path=rotated,
                    detector_backend="mtcnn",  # Use mtcnn instead of opencv
                    enforce_detection=False,
                    align=True
                )
                
                if faces and faces[0]["confidence"] > 0.97:
                    best_face = faces[0]
                    break

            except Exception as e:
                continue

        # --- Result Handling ---
        if best_face:
            area = best_face["facial_area"]
            y1, x2, y2, x1 = area["y"], area["x"]+area["w"], area["y"]+area["h"], area["x"]
            encoding = face_recognition.face_encodings(rotated, [(y1, x2, y2, x1)])[0]
            result_queue.put(([(y1, x2, y2, x1)], [encoding]))
        else:
            result_queue.put(([], []))

    except Exception as e:
        logging.error(f"Worker crashed: {e}")
        result_queue.put(([], []))

## Working code
# def process_image_worker(image_base64, result_queue):
#     """Worker function that runs in isolated process with its own memory space"""
#     try:
#         # Import dependencies inside worker
#         import gc
#         import sys
#         import torch
#         import numpy as np
#         import cv2
#         import face_recognition
#         import logging
#         from PIL import Image
#         import io
#         from concurrent.futures import ThreadPoolExecutor, as_completed
#         from deepface import DeepFace
        
#         CONFIDENCE_THRESHOLD = 0.97
        
#         def process_angle(image, angle):
#             """Process image at a specific angle for face detection"""
#             try:
#                 # Rotate image if needed
#                 if angle != 0:
#                     if angle == 90:
#                         rotated = cv2.rotate(image.copy(), cv2.ROTATE_90_CLOCKWISE)
#                     elif angle == 180:
#                         rotated = cv2.rotate(image.copy(), cv2.ROTATE_180)
#                     elif angle == 270:
#                         rotated = cv2.rotate(image.copy(), cv2.ROTATE_90_COUNTERCLOCKWISE)
#                 else:
#                     rotated = image.copy()
                
#                 # Detect faces
#                 try:
#                     face_objs = DeepFace.extract_faces(
#                         img_path=rotated,
#                         detector_backend='mtcnn',
#                         enforce_detection=False,
#                         align=True
#                     )
                
#                 except Exception as e:
#                     print(f"DeepFace.extract_faces error: {e}")
#                 confidence = face_objs[0].get('confidence', 0) if face_objs else 0
#                 # logging.info(f"Processed angle {angle} with confidence {confidence}")
                
#                 return face_objs, rotated, confidence
                
#             except Exception as e:
#                 logging.error(f"Error processing angle {angle}: {e}")
#                 return None, None, 0
#             finally:
#                 if 'rotated' in locals() and angle != 0:
#                     del rotated
#                 gc.collect()
        
#         def extract_face_data(face_objs, processed_image):
#             """Extract face locations and encodings from detected faces"""
#             try:
#                 if not face_objs:
#                     return None, None
                
#                 biggest_face = max(face_objs, key=lambda x: x['facial_area']['w'] * x['facial_area']['h'])
#                 area = biggest_face['facial_area']
#                 locations = [(area['y'], area['x'] + area['w'], area['y'] + area['h'], area['x'])]
#                 encodings = face_recognition.face_encodings(processed_image, locations)
                
#                 return (locations, encodings) if encodings else (None, None)
                
#             except Exception as e:
#                 logging.error(f"Error extracting face data: {e}")
#                 return None, None
#             finally:
#                 if 'biggest_face' in locals():
#                     del biggest_face
#                 gc.collect()
        
#         try:
#             # Handle image conversion
#             if isinstance(image_base64, bytes):
#                 image_data = image_base64
#             else:
#                 image_data = base64.b64decode(image_base64)
            
#             # Convert to PIL Image and then to numpy array
#             with Image.open(io.BytesIO(image_data)) as image_pil:
#                 image_pil = image_pil.convert('RGB')
#                 image = np.array(image_pil)
            
#             del image_data
#             # logging.info("Successfully loaded and converted image")
            
#         except Exception as e:
#             logging.error(f"Error in image conversion: {e}")
#             result_queue.put(([], []))
#             return
        
#         try:
#             # Try all angles in parallel
#             angles = [0, 90, 180, 270]
#             best_result = None
#             best_confidence = 0
            
#             with ThreadPoolExecutor(max_workers=4) as executor:
#                 # Submit all angles for processing
#                 future_to_angle = {
#                     executor.submit(process_angle, image, angle): angle 
#                     for angle in angles
#                 }
                
#                 # Process results as they complete
#                 for future in as_completed(future_to_angle):
#                     angle = future_to_angle[future]
#                     try:
#                         face_objs, processed_image, confidence = future.result()
                        
#                         if face_objs and confidence > best_confidence:
#                             # Clean up previous best result
#                             if best_result:
#                                 del best_result
                            
#                             best_result = (face_objs, processed_image, confidence, angle)
#                             best_confidence = confidence
                            
#                             # If confidence is good enough, cancel remaining tasks
#                             if confidence >= CONFIDENCE_THRESHOLD:
#                                 for f in future_to_angle:
#                                     if not f.done():
#                                         f.cancel()
#                                 break
                            
#                     except Exception as e:
#                         logging.error(f"Error processing angle {angle}: {e}")
#                         continue
#                     finally:
#                         gc.collect()
            
#             # Process best result
#             if best_result:
#                 face_objs, processed_image, confidence, angle = best_result
#                 locations, encodings = extract_face_data(face_objs, processed_image)
                
#                 if locations and encodings:
#                     logging.info(f"Best face found at angle {angle} with confidence {confidence}")
#                     result_queue.put((locations, encodings))
#                     return
            
#             logging.warning("No valid faces found in any orientation")
#             result_queue.put(([], []))
            
#         except Exception as e:
#             logging.error(f"Error in face detection/encoding: {e}")
#             result_queue.put(([], []))
            
#         finally:
#             # Cleanup
#             for var in ['image', 'best_result', 'face_objs', 'processed_image']:
#                 if var in locals():
#                     del locals()[var]
#             gc.collect()
#             if torch.cuda.is_available():
#                 torch.cuda.empty_cache()
                
#     except Exception as e:
#         logging.error(f"Critical error in worker: {e}")
#         result_queue.put(([], []))
#     finally:
#         gc.collect()

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
            # logging.info(f"Face detection completed. Locations: {result[0]}")
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



def calculate_similarity(face_encoding1, face_encoding2):
    import face_recognition
    similarity_score = 1 - face_recognition.face_distance([face_encoding1], face_encoding2)[0]

    return round(similarity_score + 0.25, 2)

def extract_face_and_compute_similarity(front_face_locations, front_face_encodings, back_face_locations, back_face_encodings):
    largest_face_index1 = front_face_locations.index(max(front_face_locations, key=lambda loc: (loc[2] - loc[0]) * (loc[3] - loc[1])))
    largest_face_index2 = back_face_locations.index(max(back_face_locations, key=lambda loc: (loc[2] - loc[0]) * (loc[3] - loc[1])))

    face_encoding1 = front_face_encodings[largest_face_index1]
    face_encoding2 = back_face_encodings[largest_face_index2]

    similarity_score = calculate_similarity(face_encoding1, face_encoding2)

    return min(1, similarity_score)
    