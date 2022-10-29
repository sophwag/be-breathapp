from flask import Flask, send_from_directory, Blueprint, request, jsonify, make_response, abort
import requests
from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import speedup
import os
from dotenv import load_dotenv
load_dotenv()

custom_audio_bp = Blueprint("custom_audio", __name__, url_prefix="/custom_audio")

# Speed change function from pydub creator https://stackoverflow.com/questions/43408833/how-to-increase-decrease-playback-speed-on-wav-file
def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })

    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

@custom_audio_bp.route("", methods = ["GET"])
def get_custom_audio():
    request_body = request.args

    # Get the desired audio type
    inhale_file_path = f'app/{request_body["sound"]}_rise.wav'
    exhale_file_path = f'app/{request_body["sound"]}_fall.wav'
    inhale = AudioSegment.from_file(inhale_file_path, format="wav")
    exhale = AudioSegment.from_file(exhale_file_path, format="wav")
    
    # Create the base pattern
    breath_part_lengths = [int(l) for l in request_body["pattern"].split("-")]
    if breath_part_lengths[0] == 0:
        stretched_inhale = AudioSegment.silent(duration=0)
    else:
        stretched_inhale = speed_change(inhale,(inhale.duration_seconds/breath_part_lengths[0])).fade_in(200).fade_out(200)
    
    if breath_part_lengths[2] == 0:
        stretched_exhale = AudioSegment.silent(duration=0)
    else:
        stretched_exhale = speed_change(exhale,(exhale.duration_seconds/breath_part_lengths[2])).fade_in(200).fade_out(200)

    stretched_inhale_pause = AudioSegment.silent(duration=(1000*breath_part_lengths[1]))
    stretched_exhale_pause = AudioSegment.silent(duration=(1000*breath_part_lengths[3]))
    base_pattern = stretched_inhale + stretched_inhale_pause + stretched_exhale + stretched_exhale_pause

    # Loop the base pattern for the desired duration
    requested_duration_secs = int(request_body["duration"])*60
    times_to_loop = int(requested_duration_secs // base_pattern.duration_seconds) + 1
    final_audio = base_pattern * times_to_loop

    # Export the custom audio
    new_file_name = f'{request_body["sound"]}_{request_body["pattern"]}_{request_body["duration"]}min.wav'
    new_file_path = f'app/{new_file_name}'
    final_audio.export(new_file_path, format="wav")

    # Retrieve and send the exported audio file
    path = os.environ.get("TEST_SOUND_PATH")
    try:
        return send_from_directory(path, filename=new_file_name, as_attachment=True)
    except FileNotFoundError:
        abort(404, description ="An error occurred while generating the audio file.")