# FaceRec

A Python‐based face recognition system with integrated liveness detection. FaceRec lets you:

- **Detect** faces in images and video streams using OpenCV’s DNN face detector.
- **Encode** known faces into 128-dimensional embeddings with the `face_recognition` library.
- **Recognize** those faces in real time from your webcam or video feed.
- **Prevent spoofing** by running a pre-trained Keras liveness model on each detected face.

---

## 📋 Features

- **Face Detection**  
  Uses OpenCV’s Caffe-based detector (`deploy.prototxt` + `res10_300x300_ssd_iter_140000.caffemodel`).

- **Face Encoding**  
  Scans a folder of labeled face images and builds `encodings.pickle` for later recognition (`encode_faces.py`).

- **Real-Time Recognition**  
  Matches live webcam faces against your known encodings.

- **Liveness Detection**  
  Runs each detected face through `liveness.h5` to reject photos/videos.

- **Utility Scripts**  
  - `balance.sh` — helper script (e.g., to rebalance datasets).  
  - `encode_faces.py` — batch-encode your “known” faces.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**  
- **dlib** (for `face_recognition`)  
- **face_recognition**  
- **OpenCV-Python**  
- **TensorFlow / Keras**  
- **imutils**, **numpy**, **scikit-learn**

### Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/MuhammedZhumali/FaceRec.git
   cd FaceRec

2. **Create & activate a virtual environment**  
    ```python3 -m venv venv
    source venv/bin/activate      # Linux/macOS
    # venv\Scripts\activate       # Windows PowerShell

3. **Install dependencies**
    ```pip install --upgrade pip
    pip install face_recognition opencv-python tensorflow imutils scikit-learn

## 🗄️ Prepare Your Dataset
Place your labeled face images in a folder structure like:
dataset/
├── alice/
│   ├── alice1.jpg
│   └── alice2.jpg
└── bob/
    ├── bob1.jpg
    └── bob2.jpg


## 🔧 Encode Known Faces
Run the encoding script to generate encodings.pickle:
    ```python encode_faces.py \
    --dataset dataset \
    --encodings encodings.pickle \
    --prototxt deploy.prototxt \
    --model res10_300x300_ssd_iter_140000.caffemodel
--dataset : Path to your folder of face images

--encodings: Path where to store the serialized embeddings

--prototxt : Face detector model definition

--model : Pre-trained face detector weights

## 🎥 Run Real-Time Recognition
    ```python face_recognition/recognize.py \
    --encodings encodings.pickle \
    --prototxt deploy.prototxt \
    --model res10_300x300_ssd_iter_140000.caffemodel \
    --liveness liveness.h5
This will:

Open your default webcam.

Detect faces in each frame.

Check liveness (real vs. spoof).

Identify recognized faces and display names in the video window.
