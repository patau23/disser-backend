from flask import Flask
from flask_cors import CORS
from flask_cors import cross_origin
from routes.predict import predict_blueprint
from routes.webrtc import create_blueprint as create_webrtc_blueprint

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Регистрируем blueprint
app.register_blueprint(predict_blueprint, url_prefix='/api')
app.register_blueprint(create_webrtc_blueprint(), url_prefix='/api')

from flask import jsonify, Blueprint

webrtc_bp = Blueprint('webrtc', __name__)


@app.route('/test')
def test():
    return "Test successful"


if __name__ == '__main__':
    app.run(debug=True)
    print("Server is running on http://localhost:5000/api")
