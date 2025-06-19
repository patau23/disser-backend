"""Prediction using the CNN model from the disser-intox repository."""

import os
import cv2
import numpy as np
from mtcnn import MTCNN
from tensorflow.keras.models import load_model

# Load detector and model once at import time
_detector = MTCNN()
# _model_path = os.path.join(os.path.dirname(__file__), "weights", "intox_model.h5")
# _model = load_model(_model_path)


def _extract_face(frame):
    """Return the largest detected face cropped from the frame."""
    detections = _detector.detect_faces(frame)
    if not detections:
        return None
    detections.sort(key=lambda d: d["box"][2] * d["box"][3], reverse=True)
    x, y, w, h = detections[0]["box"]
    x, y = max(x, 0), max(y, 0)
    return frame[y: y + h, x: x + w]


def predict_with_model(frame):
    """Predict whether a person is drunk or sober using the CNN model."""
    face = _extract_face(frame)
    if face is None or face.size == 0:
        return "unknown"

    # face = cv2.resize(face, (100, 100))
    # tensor = face.astype("float32") / 255.0
    # tensor = np.expand_dims(tensor, axis=0)

    # preds = _model.predict(tensor)
    # idx = int(np.argmax(preds[0]))
    # return "drunk" if idx == 1 else "sober"
