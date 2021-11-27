import os
import librosa.display
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
import shutil
import random

"""
AudioFileUtil analyzes all audio files in wav format and convert all of them to mel spectrograms
It also link the audio file to a specific emotion by what directory they are in. 

The code below is based and modified from the github source by Kunal Vaidya:
https://github.com/KunalVaidya99
https://towardsdatascience.com/music-genre-recognition-using-convolutional-neural-networks-cnn-part-1-212c6b93da76

Rewrote and reformatted in object-oriented principle for future calls
"""


class AudioFileUtil:

    def __init__(self, emotion_name='positive neutral negative'):
        self.emotion_name = emotion_name
        self.emotions = self.emotion_name.split()

    """
    We make directories if they are not there. 
    However, content/input_files/ should already be there (because it stores all songs for training)
    """
    def makedir(self):
        try:
            os.makedirs('../temp')

        except FileExistsError:
            print("We already have temp directory, moving on")

        try:
            os.makedirs('../your_music')

        except FileExistsError:
            print("We already have your_music directory, moving on")

        try:
            os.makedirs('../saved_model')

        except FileExistsError:
            print("We already have saved_model directory, moving on")

        for e in self.emotions:

            try:
                audio_path = os.path.join('../content/audios', f'{e}')
                os.makedirs(audio_path)

            except FileExistsError:
                print("We already have audios directory, moving on")

            try:
                train_path = os.path.join('../content/split/spectrograms/train', f'{e}')
                os.makedirs(train_path)

            except FileExistsError:
                print("We already have train directory, moving on")

            try:
                test_path = os.path.join('../content/split/spectrograms/test', f'{e}')
                os.makedirs(test_path)

            except FileExistsError:
                print("We already have test directory, moving on")


    def split_audio(self, duration=3):
        i = 0
        for e in self.emotions:
            j = 0
            print(f"{e}")
            for filename in os.listdir(os.path.join('../content/input_files/emotions/', f"{e}")):
                song = os.path.join(f'../content/input_files/emotions/{e}', f'{filename}')
                j = j + 1
                for k in range(0, 10):
                    i = i + 1
                    # We split the audio in duration of 3 seconds, which is 3000ms.
                    # This means that we will only train the first 30 seconds of the audio
                    # 3000ms = 3 seconds for one iteration, with 10 iterations total as 30 seconds.
                    t1 = duration * 1000 * k
                    t2 = duration * 1000 * (k + 1)
                    newAudio = AudioSegment.from_wav(song)
                    new = newAudio[t1:t2]
                    new.export(f'../content/audios/{e}/{e + str(j) + str(k)}.wav', format='wav')

    def generate_spectrogram(self):
        for e in self.emotions:
            j = 0
            print(e)
            for filename in os.listdir(os.path.join('../content/audios', f"{e}")):
                song = os.path.join(f'../content/audios/{e}', f'{filename}')
                j = j + 1
                output_directory = f'../content/split/spectrograms/train/{e}/{e + str(j)}.png'
                # We need to set the duration to 3 seconds to match the split audio files method above
                self.create_mel_spectrogram(output_directory, song)

    def train_test_split(self):
        directory = '../content/split/spectrograms/train/'
        for e in self.emotions:
            filenames = os.listdir(os.path.join(directory, f"{e}"))
            random.shuffle(filenames)
            test_files = filenames[0:int(len(filenames)/3)]

            for f in test_files:
                shutil.move(directory + f"{e}" + "/" + f, "../content/split/spectrograms/test/" + f"{e}")

    def reset_train_test(self):
        directory = '../content/split/spectrograms/test/'
        for e in self.emotions:
            filenames = os.listdir(os.path.join(directory, f"{e}"))
            for f in filenames:
                shutil.move(directory + f"{e}" + "/" + f, "../content/split/spectrograms/train/" + f"{e}")

    @staticmethod
    def create_mel_spectrogram(output_directory, song, duration=3):
        y, sr = librosa.load(song, duration=duration)
        mels = librosa.feature.melspectrogram(y=y, sr=sr)
        plt.Figure()
        plt.imshow(librosa.power_to_db(mels, ref=np.max))
        plt.axis('off')
        plt.savefig(output_directory)

    """
    Given the folder, convert all songs in that folder to wav format and save it in the same folder
    """
    @staticmethod
    def convertToWAV(folder):
        songs = os.listdir(folder)
        for song in songs:
            # personally i hate how mac add this file and cause so many problems
            if song == '.DS_Store':
                continue
            # check if it already is in the correct format
            filename, file_ext = os.path.splitext(song)
            if file_ext == ".wav":
                continue
            sound = AudioSegment.from_file(folder + song)
            sound.export(folder + filename + '.wav', format="wav")
            os.remove(os.path.join(folder, song))
