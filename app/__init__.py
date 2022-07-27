from flask import Flask
# not sure if I need to add these
# import os
# from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)
    # Register Blueprints here
    from app.routes import test_sounds_bp
    app.register_blueprint(test_sounds_bp)
    
    # not sure if I need this
    #CORS(app)
    return app