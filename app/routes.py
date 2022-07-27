from flask import Blueprint, request, jsonify, make_response, abort
import requests
import os
from pydub import AudioSegment
from pydub.playback import play

sound = AudioSegment.from_file("app/sample_sound.wav", format="wav")
# play(sound)

short = sound[:1000]
# play(short)

test_sounds_bp = Blueprint("test_sounds", __name__, url_prefix="/test_sounds")


@test_sounds_bp.route("", methods = ["GET"])
def get_test_sound():
    request_body = request.get_json()
    test_sound = sound
    test_dict = {"key":"test value"}
    
    return jsonify(test_dict)