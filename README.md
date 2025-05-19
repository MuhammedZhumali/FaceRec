# FaceRec

**FaceRec** is a Python-based facial recognition system enhanced with liveness detection. It enables secure authentication by identifying faces from a known database and ensuring the subject is a real, live person.

## 📁 Project Structure

├── Main.py # Main script to run face recognition

├── encode_faces.py # Script to generate face encodings

├── encodings.pickle # Saved face embeddings

├── face_recognition # Binary/script for face recognition execution

├── liveness_model_softmax.h5 # Trained Keras model for liveness detection

├── balance.sh # Shell script (possibly for setup or balance config)

├── bin/, share/ # Possibly environment or system folders

├── pyvenv.cfg # Python virtual environment configuration

└── README.md # Project description and instructions


## 🧠 Features

- Face detection using Haar cascades or CNNs (based on implementation).
- Face recognition using embeddings and cosine distance comparison.
- Liveness detection using a trained softmax-based deep learning model.
- Encodings stored as a `.pickle` file for fast access.
- Simple command-line execution.

## ⚙️ Requirements

- Python 3.11+
- OpenCV
- `face_recognition`
- `numpy`, `dlib`, `tensorflow`, `keras`

## 🚀 Usage
### 1. Encode known faces:
Place labeled face images into a dataset folder:
dataset/
├── Alice/
│   └── alice1.jpg
├── Bob/
│   └── bob1.jpg

Then run:
python encode_faces.py

This will generate encodings.pickle.

### 2. Start recognition:
python face_recognition.py
python Main.py(system with ultrasonic sensor)

## 🧪 Liveness Detection
The model liveness_model_softmax.h5 is a trained binary classifier that detects real vs. spoofed (photo/video) faces. It works in conjunction with the real-time recognition process to prevent spoofing.



## 🛠 Dev Notes
The folders bin/ and share/man/ might come from a Linux package or installed CLI tool.
face_recognition may be a binary or renamed script.

