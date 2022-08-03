from flask import Flask, send_from_directory, Blueprint, request, jsonify, make_response, abort
import requests
import time
from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import speedup
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
custom_audio_bp = Blueprint("custom_audio", __name__, url_prefix="/custom_audio")

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

# from pydub creator https://stackoverflow.com/questions/43408833/how-to-increase-decrease-playback-speed-on-wav-file
def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })

    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

# route that creates custom audio
@custom_audio_bp.route("", methods = ["GET"])
def get_custom_audio():
    request_body = request.args

    #getting the root inhale and exhale sounds
    if request_body["sound"] == "test":
        inhale = AudioSegment.from_file("app/sample_sound.wav", format="wav")
        exhale = AudioSegment.from_file("app/sample_sound.wav", format="wav")
    elif request_body["sound"] == "synth":
        inhale = AudioSegment.from_file("app/synth_rise.wav", format="wav")
        exhale = AudioSegment.from_file("app/synth_fall.wav", format="wav")
    
    #create the base pattern
    breath_part_lengths = [int(l) for l in request_body["pattern"].split("-")]
    if breath_part_lengths[0] == 0:
        stretched_inhale = AudioSegment.silent(duration=0)
    else:
        stretched_inhale = speed_change(inhale,(inhale.duration_seconds/breath_part_lengths[0]))
    
    if breath_part_lengths[2] == 0:
        stretched_exhale = AudioSegment.silent(duration=0)
    else:
        stretched_exhale = speed_change(exhale,(exhale.duration_seconds/breath_part_lengths[2]))

    stretched_inhale_pause = AudioSegment.silent(duration=(1000*breath_part_lengths[1]))
    stretched_exhale_pause = AudioSegment.silent(duration=(1000*breath_part_lengths[3]))
    
    base_pattern = stretched_inhale + stretched_inhale_pause + stretched_exhale + stretched_exhale_pause

    #loop the base pattern
    requested_duration_secs = int(request_body["duration"])*60
    times_to_loop = int(requested_duration_secs // base_pattern.duration_seconds) + 1
    final_audio = base_pattern * times_to_loop

    #export the custom audio
    new_file_name = f'{request_body["sound"]}_{request_body["pattern"]}_{request_body["duration"]}min.wav'
    new_file_path = f'app/{new_file_name}'
    final_audio.export(new_file_path, format="wav")

    #retrieve and send the exported audio file
    path = os.environ.get("TEST_SOUND_PATH")
    try:
        return send_from_directory(path, filename=new_file_name, as_attachment=True)
    except FileNotFoundError:
        abort(404, description ="File not found")