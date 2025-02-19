import cv2
import numpy as np
import os
import shutil
from pathlib import Path

# Ścieżki
IMAGE_DIR = "/path/to/your/images"  # Folder z obrazami do przeszukania
SAMPLE_IMAGE = "/path/to/sample.png"  # Wzorcowy element
RESULTS_DIR = "./cleanedResults"  # Folder na wycięte elementy

# Tworzenie folderu na wyniki
os.makedirs(RESULTS_DIR, exist_ok=True)

def extract_matching_region(image_path, sample, threshold=0.8):
    """Wyszukuje wzorzec w obrazie i zwraca wycięty fragment."""
    img = cv2.imread(image_path)
    sample_gray = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Dopasowanie wzorca metodą Template Matching
    result = cv2.matchTemplate(img_gray, sample_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Sprawdzenie, czy dopasowanie jest wystarczająco dobre
    if max_val >= threshold:
        h, w = sample_gray.shape
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # Wycięcie regionu
        cropped = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        return cropped
    return None

def process_images(image_dir, sample_path, results_dir):
    """Przetwarza obrazy, wyszukuje wzorzec i zapisuje wycięte elementy."""
    sample = cv2.imread(sample_path)

    for image_path in Path(image_dir).glob("*"):
        if image_path.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
            cropped_region = extract_matching_region(str(image_path), sample)
            
            if cropped_region is not None:
                output_path = os.path.join(results_dir, image_path.name)
                cv2.imwrite(output_path, cropped_region)
                print(f"Zapisano: {output_path}")

# Uruchomienie programu
process_images(IMAGE_DIR, SAMPLE_IMAGE, RESULTS_DIR)

print("✅ Proces zakończony. Wycięte elementy znajdują się w ./cleanedResults")
