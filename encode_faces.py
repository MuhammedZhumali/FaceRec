#!/usr/bin/env python3
import os
import cv2
import pickle
import bcrypt
import face_recognition

dataset_path = "origdataset"   # each subfolder is a passport ID containing .jpg images
encodings    = []
hashed_names = []

# Generate one salt for the entire dataset
salt = bcrypt.gensalt()

for passport in os.listdir(dataset_path):
    ppath = os.path.join(dataset_path, passport)
    if not os.path.isdir(ppath):
        continue

    print(f"[INFO] Processing passport: {passport}")
    for img_name in os.listdir(ppath):
        img_path = os.path.join(ppath, img_name)
        image = cv2.imread(img_path)
        if image is None:
            print(f"[WARN] Could not read {img_path}")
            continue

        # detect & encode faces
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model="hog")
        if not boxes:
            print(f"[WARN] No face found in {img_path}")
            continue

        for enc in face_recognition.face_encodings(rgb, boxes):
            encodings.append(enc)
            hashed = bcrypt.hashpw(passport.encode(), salt)
            hashed_names.append(hashed)

print(f"[INFO] Collected {len(encodings)} face encodings")

if encodings:
    with open("encodings.pickle", "wb") as f:
        pickle.dump({
            "encodings":    encodings,
            "hashed_names": hashed_names,
            "salt":         salt
        }, f)
    print("[INFO] Saved encodings.pickle")
else:
    print("[ERROR] No encodings to save, check your dataset")