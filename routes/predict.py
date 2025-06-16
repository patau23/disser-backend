from flask import Blueprint, request, jsonify
from models.drunkselfie_model import predict_with_model
from utils.preprocess import preprocess_image

predict_blueprint = Blueprint('predict', __name__)


@predict_blueprint.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    image = request.files['file'].read()
    frame = preprocess_image(image)

    result = predict_with_model(frame)

    return jsonify({'result': result})
