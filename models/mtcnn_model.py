"""Prediction utilities using the models from the disser-mtcnn repository."""

import os
import cv2
import numpy as np
from mtcnn import MTCNN
import joblib
from tensorflow.keras.models import load_model

# Initialize detector and load models once
_detector = MTCNN()
_svm_path = os.path.join(os.path.dirname(__file__), "weights", "drunk_svm.joblib")
_mlp_path = os.path.join(os.path.dirname(__file__), "weights", "facial_drunk.keras")
_svm_model = joblib.load(_svm_path)
_mlp_model = load_model(_mlp_path)


def _extract_face(frame):
    detections = _detector.detect_faces(frame)
    if not detections:
        return None
    detections.sort(key=lambda d: d["box"][2] * d["box"][3], reverse=True)
    x, y, w, h = detections[0]["box"]
    x, y = max(x, 0), max(y, 0)
    return frame[y: y + h, x: x + w]


def _preprocess(face):
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (96, 96))
    return resized.astype("float32") / 255.0


def predict_with_model(frame, method="svm"):
    """Predict intoxication using either the SVM or MLP model."""
    face = _extract_face(frame)
    if face is None or face.size == 0:
        return "unknown"

    arr = _preprocess(face)

    if method == "mlp":
        tensor = arr.reshape(1, 96, 96, 1)
        preds = _mlp_model.predict(tensor)
        if preds.shape[-1] == 1:
            prob = preds[0][0]
            return "drunk" if prob >= 0.5 else "sober"
        idx = int(np.argmax(preds[0]))
        return "drunk" if idx == 1 else "sober"

    flat = arr.flatten().reshape(1, -1)
    pred = _svm_model.predict(flat)[0]
    return "drunk" if pred == 1 or str(pred).lower() == "drunk" else "sober"
