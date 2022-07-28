from flask import Flask
# not sure if I need to add these
# import os
# from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)
    # Register Blueprints here
    from app.routes import test_dict_bp
    app.register_blueprint(test_dict_bp)
    from app.routes import test_audio_bp
    app.register_blueprint(test_audio_bp)
    from app.routes import test_image_bp
    app.register_blueprint(test_image_bp)
    from app.routes import test_edited_sound_bp
    app.register_blueprint(test_edited_sound_bp)
    from app.routes import test_edited_long_sound_bp
    app.register_blueprint(test_edited_long_sound_bp)
    from app.routes import test_edited_medium_sound_bp
    app.register_blueprint(test_edited_medium_sound_bp)
    
    # not sure if I need this
    #CORS(app)
    return app