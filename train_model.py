import cv2
import os
import numpy as np
from PIL import Image
import json

# Create LBPH recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

dataset_path = "dataset"

faces = []
labels = []

label_map = {}
current_label = 0

# Loop through each student folder
for folder in sorted(os.listdir(dataset_path)):
    folder_path = os.path.join(dataset_path, folder)

    if not os.path.isdir(folder_path):
        continue

    # Assign an ID automatically
    label_map[current_label] = folder

    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)

        img = Image.open(image_path).convert("L")
        img_numpy = np.array(img, "uint8")

        faces.append(img_numpy)
        labels.append(current_label)

    current_label += 1

# Train the recognizer
recognizer.train(faces, np.array(labels))

# Save the trained model
recognizer.save("trainer.yml")

# Save the ID -> Name mapping
with open("labels.json", "w") as f:
    json.dump(label_map, f)

print("✅ Model trained successfully!")
print("✅ labels.json created.")