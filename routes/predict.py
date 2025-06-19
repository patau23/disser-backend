from flask import Blueprint, request, jsonify
from models.drunkselfie_model import predict_with_model as intox_predict
from models.mtcnn_model import predict_with_model as mtcnn_predict
from utils.preprocess import preprocess_image

predict_blueprint = Blueprint('predict', __name__)


@predict_blueprint.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    image = request.files['file'].read()
    frame = preprocess_image(image)

    model_name = request.form.get('model', 'intox')
    method = request.form.get('method', 'svm')

    if model_name == 'mtcnn':
        result = mtcnn_predict(frame, method=method)
    else:
        result = mtcnn_predict(frame, method=method)
        # result = intox_predict(frame)

    return jsonify({'result': result})
