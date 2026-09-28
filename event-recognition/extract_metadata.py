import os
import json
import argparse
import numpy as np
import piexif
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

MODEL_PATH = "event_classifier_model.h5"
LABELS_PATH = "class_labels.json"
IMG_SIZE = (224, 224)


def load_labels():
    with open(LABELS_PATH) as f:
        raw = json.load(f)
        return {int(k): v for k, v in raw.items()}


def predict_event(model, label_map, image_path):
    img = Image.open(image_path).convert("RGB").resize(IMG_SIZE)
    arr = img_to_array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)

    prob = model.predict(arr, verbose=0)[0][0]
    predicted_class = 1 if prob >= 0.5 else 0
    confidence = prob if predicted_class == 1 else 1 - prob

    return label_map[predicted_class], round(float(confidence) * 100, 2)


def write_exif_tag(image_path, event_name):
    try:
        exif_dict = piexif.load(image_path)
    except Exception:
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = f"event:{event_name}".encode()
    piexif.insert(piexif.dump(exif_dict), image_path)


def main(input_dir):
    model = load_model(MODEL_PATH)
    label_map = load_labels()

    results = []
    for filename in sorted(os.listdir(input_dir)):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        image_path = os.path.join(input_dir, filename)
        event_name, confidence = predict_event(model, label_map, image_path)

        if filename.lower().endswith((".jpg", ".jpeg")):
            write_exif_tag(image_path, event_name)

        results.append({"filename": filename, "event": event_name, "confidence_percent": confidence})
        print(f"{filename}: {event_name} ({confidence}% confidence)")

    out_path = os.path.join(input_dir, "metadata.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nMetadata for {len(results)} images saved to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True, help="Folder of NEW images to tag")
    args = parser.parse_args()
    main(args.input_dir)