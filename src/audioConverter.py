import subprocess
import os

from pydub import AudioSegment

"""
This is for windows since windows required ffmpeg as separate executable
"""
def convert_to_wav_windows(filepath, save_to):
    # check if it already is in the correct format
    filename, file_ext = os.path.splitext(filepath)
    if file_ext == ".wav":
        return
    # otherwise use ffmpeg to convert the file to wav
    subprocess.run([
        "ffmpeg", "-y",
        "-i",
        filepath,
        os.path.join(save_to + ".wav")
    ])


"""
Given a filepath, convert one song to wav format and save to another folder
This is for machines other than windows. 
"""
def convert_to_wav(filepath, save_to):
    # check if it already is in the correct format
    filename, file_ext = os.path.splitext(filepath)
    if file_ext == ".wav":
        return
    # otherwise use ffmpeg to convert the file to wav
    sound = AudioSegment.from_file(filepath)
    sound.export(save_to + '.wav', format="wav")
