from flask import Flask
import os
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)

    from app.routes import custom_audio_bp
    app.register_blueprint(custom_audio_bp)
    
    CORS(app)
    return app