from flask import Flask, render_template, send_from_directory, request, send_file
import os
import random
from pydub import AudioSegment
from keras_preprocessing import image
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../src')
from downloadSongURL import getAudioFile
from audioConverter import convert_to_wav, convert_to_wav_windows

import os
from keras_preprocessing.image import load_img
from shutil import copyfile
import AudioFileUtil
import NeuralAgent

app = Flask(__name__)
audio_utility = AudioFileUtil.AudioFileUtil()
my_agent = NeuralAgent.NeuralAgent()
try:
    my_agent.load_model()
except FileNotFoundError:
    raise FileNotFoundError('No existing model presents! Please create a new model from main.py!')

if not os.path.exists('user_songs'):
    os.makedirs('user_songs')

if not os.path.exists('user_songs/temp/song_output'):
    os.makedirs('user_songs/temp/song_output')

if not os.path.exists("user_songs/temp"):
    os.makedirs("user_songs/temp")

if not os.path.exists("user_songs/regular"):
    os.makedirs("user_songs/regular")

if not os.path.exists("user_songs/wav"):
    os.makedirs("user_songs/wav")

@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('assets', path)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/content/input_files/emotions/positive/<path:filename>')
def download_file_positive(filename):
    return send_from_directory('../content/input_files/emotions/positive/', filename)

@app.route('/content/input_files/emotions/negative/<path:filename>')
def download_file_negative(filename):
    return send_from_directory('../content/input_files/emotions/negative/', filename)

@app.route('/content/input_files/emotions/neutral/<path:filename>')
def download_file_neutral(filename):
    return send_from_directory('../content/input_files/emotions/neutral/', filename)

@app.route('/user_songs/wav/<path:filename>')
def download_file_user_song(filename):
    print("LOOKIN FOR WWAV")
    return send_from_directory('user_songs/wav/', filename)

@app.route("/", methods=['POST'])
def button_pressed_emotions():

    if request.form["moodBtn"] == "Positive":
        print("THEY CLICKED THE DANG POSITIVE BUTTON")
        songs = os.listdir("../content/input_files/emotions/positive/")
        song = random.choice(songs)
        song_url = "/content/input_files/emotions/positive/{}".format(song)
        return render_template('index.html', song_name=song.replace(".wav", ""), song_url=song_url)
    
    elif request.form["moodBtn"] == "Neutral":
        print("THEY CLICKED THE DANG NEUTRAL BUTTON")
        songs = os.listdir("../content/input_files/emotions/neutral/")
        song = random.choice(songs)
        song_url = "/content/input_files/emotions/neutral/{}".format(song)
        return render_template('index.html', song_name=song.replace(".wav", ""), song_url=song_url)
    
    elif request.form["moodBtn"] == "Negative":
        print("THEY CLICKED THE DANG NEGATIVE BUTTON")
        songs = os.listdir("../content/input_files/emotions/negative/")
        song = random.choice(songs)
        song_url = "/content/input_files/emotions/negative/{}".format(song)
        return render_template('index.html', song_name=song.replace(".wav", ""), song_url=song_url)
    
    else:
        print("THEY CLICKED THE DANG NO  BUTTON")
        return render_template(
            'index.html',
            song_name="",
            song_url=""
        )

@app.route("/user_song", methods=['POST'])
def button_pressed_add_my_song():
    user_song_url = request.form["yt_link"].strip()
    title = getAudioFile([user_song_url], "user_songs/regular")
    song_url = ""

    for song_title in os.listdir("user_songs/regular"):
        if title in song_title:
            convert_to_wav("user_songs/regular/{}".format(song_title), "user_songs/wav/{}".format(title))
            os.remove("user_songs/regular/{}".format(song_title))
            song_url = "/user_songs/wav/{}.wav".format(title)
            break
    
    class_label_list = []
    class_labels = my_agent.get_class_labels()
    duration = 3
    song_directory = "user_songs/wav/{}.wav".format(title)
    for k in range(0, 10):
        t1 = duration * 1000 * k
        t2 = duration * 1000 * (k + 1)
        newAudio = AudioSegment.from_wav(song_directory)
        new = newAudio[t1:t2]
        split_directory = f'user_songs/temp/{str(song_title) + str(k)}.wav'
        new.export(split_directory, format='wav')
        audio_utility.create_mel_spectrogram('user_songs/temp/song_output/song_output' + str(k) + '.png', split_directory)

    for k in range(0, 10):
        image_data = image.load_img('user_songs/temp/song_output/song_output' + str(k) + '.png', color_mode='rgba',
                                    target_size=(288, 432))
        class_label, prediction = my_agent.predict(image_data)
        class_label_list.append(class_label)
        os.remove("user_songs/temp/" + str(song_title) + str(k) + ".wav")
        os.remove('user_songs/temp/song_output/song_output' + str(k) + '.png')

    # render template
    return render_template(
        'index.html',
        song_name=title,
        song_url=song_url,
        probability_positive= str(class_label_list.count(2) / 10 * 100) + "%",
        probability_neutral= str(class_label_list.count(1) / 10 * 100) + "%",
        probability_negative= str(class_label_list.count(0) / 10 * 100) + "%"
    )

if __name__ == '__main__':
   app.run()