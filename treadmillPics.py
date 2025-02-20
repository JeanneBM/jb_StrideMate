## uzywa wbudowanej wiedzy a nie przykladowego obrazu

import os
import shutil
from PIL import Image
import torch
from torchvision import models, transforms

# Ścieżki do folderów
SOURCE_FOLDER = "sciezka_do_zrodlowego_folderu"
DEST_FOLDER = "sciezka_do_docelowego_folderu"

# Tworzenie folderu docelowego, jeśli nie istnieje
os.makedirs(DEST_FOLDER, exist_ok=True)

# Ładowanie modelu
model = models.mobilenet_v2(pretrained=True)
model.eval()

# Transformacja obrazu
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Pobranie etykiet ImageNet
LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
LABELS_FILE = "imagenet_classes.txt"
if not os.path.exists(LABELS_FILE):
    import urllib.request
    urllib.request.urlretrieve(LABELS_URL, LABELS_FILE)

with open(LABELS_FILE) as f:
    labels = [line.strip() for line in f.readlines()]

# Kluczowe słowa związane z siłownią
GYM_KEYWORDS = {"gym", "fitness", "workout", "exercise", "treadmill"}

# Przetwarzanie zdjęć
for filename in os.listdir(SOURCE_FOLDER):
    if filename.lower().endswith((".jpg")):
        img_path = os.path.join(SOURCE_FOLDER, filename)
        image = Image.open(img_path).convert("RGB")
        img_tensor = transform(image).unsqueeze(0)
        
        with torch.no_grad():
            outputs = model(img_tensor)
            _, predicted = outputs.max(1)
            label = labels[predicted.item()]
        
        # Sprawdzanie, czy etykieta pasuje do siłowni
        if any(keyword in label.lower() for keyword in GYM_KEYWORDS):
            shutil.copy(img_path, os.path.join(DEST_FOLDER, filename))
            print(f"Skopiowano: {filename} ({label})")

print("Zakończono przetwarzanie.")
