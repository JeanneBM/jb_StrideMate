import cv2
import numpy as np
import os
import shutil
from pathlib import Path
import imagehash
from PIL import Image

# Ścieżki
IMAGE_DIR = "/path/to/your/images"  # Folder z obrazami do przeszukania
REFERENCE_IMAGE = "/mnt/data/image.png"  # Wzorcowy obraz
RESULTS_DIR = "./Results"  # Folder do zapisu podobnych zdjęć

# Tworzenie folderu na wyniki, jeśli nie istnieje
os.makedirs(RESULTS_DIR, exist_ok=True)

def compute_hash(image_path):
    """Oblicza hash percepcyjny obrazu."""
    img = Image.open(image_path)
    return imagehash.phash(img)

def find_and_copy_similar_images(reference_image, directory, results_dir, threshold=5):
    """Znajduje podobne obrazy i kopiuje je do katalogu wynikowego."""
    ref_hash = compute_hash(reference_image)
    similar_images = []

    for image_path in Path(directory).glob("*"):
        if image_path.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
            img_hash = compute_hash(image_path)
            if abs(ref_hash - img_hash) <= threshold:
                similar_images.append(str(image_path))
                shutil.copy(image_path, results_dir)  # Kopiowanie obrazu

    return similar_images

# Uruchomienie funkcji
similar_images = find_and_copy_similar_images(REFERENCE_IMAGE, IMAGE_DIR, RESULTS_DIR)

# Wynik
print("Podobne obrazy skopiowane do folderu ./Results:")
for img in similar_images:
    print(img)
