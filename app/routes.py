from flask import Flask, send_from_directory, Blueprint, request, jsonify, make_response, abort
import requests
import time
from pydub import AudioSegment
from pydub.playback import play
import os
from dotenv import load_dotenv
load_dotenv()

#blueprints
test_dict_bp = Blueprint("test_dict", __name__, url_prefix="/test_dict")
test_audio_bp = Blueprint("test_audio", __name__, url_prefix="/test_audio")
test_image_bp = Blueprint("test_image", __name__, url_prefix="/test_image")
test_edited_sound_bp = Blueprint("test_edited_sound", __name__, url_prefix="/test_edited_sound")
test_edited_long_sound_bp = Blueprint("test_edited_long_sound", __name__, url_prefix="/test_edited_long_sound")
test_edited_medium_sound_bp = Blueprint("test_edited_medium_sound", __name__, url_prefix="/test_edited_medium_sound")


#route that returns a dictionary
@test_dict_bp.route("", methods = ["GET"])
def get_test_dict():
    request_body = request.get_json()
    test_dict = {"key":"test value"}
    return jsonify(test_dict)

#route that returns an image
@test_image_bp.route("", methods = ["GET"])
def get_test_image():
    path = os.environ.get("TEST_SOUND_PATH")
    try:
        return send_from_directory(path, filename="sample_image.jpg", as_attachment=True)
    except FileNotFoundError:
        abort(404)

#route that returns an audio file that already existed
@test_audio_bp.route("", methods = ["GET"])
def get_test_audio():
    path = os.environ.get("TEST_SOUND_PATH")
    try:
        return send_from_directory(path, filename="sample_sound.wav", as_attachment=True)
    except FileNotFoundError:
        abort(404)

#route that creates and returns a short audio file
@test_edited_sound_bp.route("", methods = ["GET"])
def get_test_edited_sound():
    sound = AudioSegment.from_file("app/sample_sound.wav", format="wav")
    short = sound[:1000]
    short.export("app/new_audio.wav", format="wav")
    path = os.environ.get("TEST_SOUND_PATH")
    try:
        return send_from_directory(path, filename="new_audio.wav", as_attachment=True)
    except FileNotFoundError:
        abort(404, description ="File not found")


#route that creates and returns a long audio file
@test_edited_long_sound_bp.route("", methods = ["GET"])
def get_test_edited_long_sound():
    sound = AudioSegment.from_file("app/sample_sound.wav", format="wav")
    long = sound * 450
    long.export("app/new_long_audio.wav", format="wav")
    # time.sleep(5)
    path = os.environ.get("TEST_SOUND_PATH")
    try:
        return send_from_directory(path, filename="new_long_audio.wav", as_attachment=True)
    except FileNotFoundError:
        abort(404, description ="File not found")

#route that creates and returns a 10-minute audio file
@test_edited_medium_sound_bp.route("", methods = ["GET"])
def get_test_edited_medium_sound():
    sound = AudioSegment.from_file("app/sample_sound.wav", format="wav")
    long = sound * 75
    long.export("app/new_medium_audio.wav", format="wav")
    # time.sleep(5)
    path = os.environ.get("TEST_SOUND_PATH")
    try:
        return send_from_directory(path, filename="new_medium_audio.wav", as_attachment=True)
    except FileNotFoundError:
        abort(404, description ="File not found")