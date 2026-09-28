"""
Simplest version — just run this file, it will ASK you for the image path,
then tell you which event it thinks it is.

USAGE:
    python predict_simple.py
    (then type or paste the image path when it asks)
"""

import json
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

MODEL_PATH = "event_classifier_model.h5"
LABELS_PATH = "class_labels.json"
IMG_SIZE = (224, 224)
print(1)
# Load model + labels once
model = load_model(MODEL_PATH)
with open(LABELS_PATH) as f:
    raw = json.load(f)
    label_map = {int(k): v for k, v in raw.items()}
print(2)
# Ask user for image path
image_path = input("Enter image path: ").strip('"')  # strip() removes quotes if pasted from Windows

# Prepare image same way as training
img = Image.open(image_path).convert("RGB").resize(IMG_SIZE)
arr = img_to_array(img) / 255.0
arr = np.expand_dims(arr, axis=0)
print(3)
# Predict
prob = model.predict(arr, verbose=0)[0][0]
predicted_class = 1 if prob >= 0.5 else 0
confidence = prob if predicted_class == 1 else 1 - prob
event_name = label_map[predicted_class]
print(4)
print(f"\nPredicted event: {event_name}")
print(f"Confidence: {round(float(confidence) * 100, 2)}%")