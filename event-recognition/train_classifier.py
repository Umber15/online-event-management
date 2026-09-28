import json
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator

DATASET_DIR = "dataset"      # contains birthday/ and convocation/
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 10
MODEL_OUT = "event_classifier_model.h5"
LABELS_OUT = "class_labels.json"

datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2,     # 80% train, 20% validation
    rotation_range=15,
    zoom_range=0.15,
    horizontal_flip=True,
)

train_data = datagen.flow_from_directory(
    DATASET_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE,
    class_mode="binary", subset="training",
)
val_data = datagen.flow_from_directory(
    DATASET_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE,
    class_mode="binary", subset="validation",
)

# Save which number means which folder/event, e.g. {"0": "birthday", "1": "convocation"}
label_map = {v: k for k, v in train_data.class_indices.items()}
with open(LABELS_OUT, "w") as f:
    json.dump(label_map, f, indent=2)
print("Class mapping:", label_map)

base_model = MobileNetV2(input_shape=IMG_SIZE + (3,), include_top=False, weights="imagenet")
base_model.trainable = False   # reuse Google's pretrained weights, don't retrain them

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(64, activation="relu"),
    layers.Dropout(0.3),
    layers.Dense(1, activation="sigmoid"),
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
model.summary()

history = model.fit(train_data, validation_data=val_data, epochs=EPOCHS)

model.save(MODEL_OUT)
print(f"Model saved to {MODEL_OUT}")
print("Final validation accuracy:", history.history["val_accuracy"][-1])