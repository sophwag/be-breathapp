from flask import Blueprint, request, jsonify, make_response, abort
import requests
import os
from pydub import AudioSegment
from pydub.playback import play

sound = AudioSegment.from_file("app/sample_sound.wav", format="wav")
# play(sound)
# test comment

short = sound[:1000]
# play(short)

test_dict_bp = Blueprint("test_dict", __name__, url_prefix="/test_dict")
test_audio_bp = Blueprint("test_audio", __name__, url_prefix="/test_audio")

@test_dict_bp.route("", methods = ["GET"])
def get_test_sound():
    request_body = request.get_json()
    test_sound = sound
    test_dict = {"key":"test value"}
    
    return jsonify(test_dict)

@test_audio_bp.route("", methods = ["GET"])
def get_test_audio():
    request_body = request.get_json()
    test_sound = sound
    test_dict = {"key":"test song"}
    
    return jsonify(test_dict)