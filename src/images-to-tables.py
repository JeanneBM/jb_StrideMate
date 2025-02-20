import cv2
import pytesseract
import pandas as pd
import json
from datetime import datetime

# Generowanie znacznika czasu
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Wczytaj obraz
image_path = "/mnt/data/Zrzut ekranu 2025-02-17 150323.jpg"
image = cv2.imread(image_path)

# Konwersja do skali szarości i binaryzacja
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# OCR - rozpoznawanie tekstu
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(gray, config=custom_config, lang="pol")

# Zapis surowego OCR tekstu (opcjonalnie)
ocr_text_path = f"/mnt/data/ocr_output_{timestamp}.txt"
with open(ocr_text_path, "w", encoding="utf-8") as f:
    f.write(text)

# Przetwarzanie tekstu na dane numeryczne
data = {}
lines = text.split("\n")
for line in lines:
    parts = line.split()
    if len(parts) > 1:
        key = " ".join(parts[:-1])  # Klucz (np. "Kalorie", "Dystans (km)")
        value = parts[-1].replace(",", ".")  # Zamiana przecinka na kropkę
        try:
            value = float(value) if "." in value else int(value)
        except ValueError:
            continue
        data[key] = value

# Konwersja do DataFrame
df = pd.DataFrame([data])

# Zapis do CSV i JSON z dynamiczną nazwą
csv_path = f"/mnt/data/dane_sagemaker_{timestamp}.csv"
json_path = f"/mnt/data/dane_sagemaker_{timestamp}.json"

df.to_csv(csv_path, index=False)
with open(json_path, "w") as json_file:
    json.dump(data, json_file)

print(f"Dane zapisane do:\n- {csv_path}\n- {json_path}\n- {ocr_text_path} (surowy tekst OCR)")
