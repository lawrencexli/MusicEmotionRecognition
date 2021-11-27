import shutil
import random

from keras_preprocessing import image
from pydub import AudioSegment

import AudioFileUtil
import NeuralAgent
import os

"""
main.py is to test whether the neural agent and audio file utility works correctly
This is a debug program
"""


class Main:

    def __init__(self):
        self.audio_utility = AudioFileUtil.AudioFileUtil()
        self.class_labels = None
        self.my_agent = None
        self.name_song = None

    def audio_option(self):
        print("Welcome to the music mood classification of music")
        if input("Do you want to erase all the spectrograms data from the previous run? (y/n)") == 'y':
            try:
                shutil.rmtree('../content/audios')

            except FileNotFoundError:
                print('The file is already deleted, moving on')

            try:
                shutil.rmtree('../content/split')

            except FileNotFoundError:
                print('The file is already deleted, moving on')

        if input("Do you want to create the spectrograms for songs? (y/n)") == 'y':
            self.audio_utility.makedir()
            self.audio_utility.split_audio()
            self.audio_utility.generate_spectrogram()
        if input("Do you want to split train and test data? (y/n)") == 'y':
            self.audio_utility.reset_train_test()
            self.audio_utility.train_test_split()

    def neural_option(self):
        self.my_agent = NeuralAgent.NeuralAgent()
        while True:
            user_input = input("Do you want to create or load model? (create/load)")
            if user_input == 'create':
                self.my_agent.create_model()
                break
            elif user_input == 'load':
                try:
                    self.my_agent.load_model()
                    break
                except FileNotFoundError:
                    print('No existing model presents! Please create a new model and train from the beginning!')
                    continue
            else:
                print("Invalid input! Please try again!")
                continue
        if input("Do you want to train the music? (y/n)") == 'y':
            self.my_agent.train()
        if input("Do you want to save the model for future use? (y/n)") == 'y':
            self.my_agent.save_model()

    def convertToWAV(self, duration=3):
        while True:
            try:
                self.audio_utility.convertToWAV('../your_music/')
                self.name_song = input("Please give the filename of your music! (NAME only no EXTENSION)")
                song_directory = '../your_music/' + self.name_song + '.wav'
                for k in range(0, 10):
                    t1 = duration * 1000 * k
                    t2 = duration * 1000 * (k + 1)
                    newAudio = AudioSegment.from_wav(song_directory)
                    new = newAudio[t1:t2]
                    split_directory = f'../temp/{str(self.name_song) + str(k)}.wav'
                    new.export(split_directory, format='wav')
                    self.audio_utility.create_mel_spectrogram('../temp/song_output' + str(k) + '.png', split_directory)
                break
            except (FileNotFoundError, IsADirectoryError):
                print("Invalid path! Please check your typing and try again!")
                continue

    def model_predict(self):
        print("We have now received your music and emotion")
        class_label_list = []
        self.class_labels = self.my_agent.get_class_labels()
        for k in range(0, 10):
            image_data = image.load_img('../temp/song_output' + str(k) + '.png', color_mode='rgba',
                                        target_size=(288, 432))
            class_label, prediction = self.my_agent.predict(image_data)
            class_label_list.append(class_label)
            os.remove("../temp/" + str(self.name_song) + str(k) + ".wav")

        print("Probability of each emotion class:")
        print("Positive: " + str(class_label_list.count(2) / 10 * 100) + "%")
        print("Neutral: " + str(class_label_list.count(1) / 10 * 100) + "%")
        print("Negative: " + str(class_label_list.count(0) / 10 * 100) + "%")

    def improvement(self):
        if input("Is our prediction correct? (y/n)") == 'y':
            print("Nice! It's pretty cool isn't it")
        else:
            print("Oh we are sorry to hear that")
            if input("Do you want to add your song to our training list? (y/n)") == 'y':
                while True:
                    emotion = input(
                        "What is the actual emotion of this song (0/1/2) [0: negative, 1: neutral, 2: positive]")
                    try:
                        emotion = int(emotion)
                        if not (emotion in [0, 1, 2]):
                            print("Invalid number input! Please input an integer (0 or 1 or 2)")
                            continue

                        filenames = os.listdir(os.path.join('../temp/'))
                        random.shuffle(filenames)
                        test_files = filenames[0:int(len(filenames) / 3)]

                        j = 0
                        for f in test_files:
                            j = j + 1
                            shutil.move('../temp/' + f, '../content/split/spectrograms/test/' +
                                        self.class_labels[emotion] + '/' + str(self.name_song) + str(j) + '.png')

                        j = 0
                        filenames = os.listdir(os.path.join('../temp/'))
                        for f in filenames:
                            j = j + 1
                            shutil.copyfile('../temp/' + f,
                                        '../content/split/spectrograms/train/' +
                                        self.class_labels[emotion] + '/' + str(self.name_song) + str(j) + '.png')
                        break
                    except ValueError:
                        print("Invalid number input! Please input an integer (0 or 1 or 2)")
                        continue
                print("We have successfully put this song into our training folder so it can improve the neural model!")


"""
Here is the main program of our project. Starts here!
"""
if __name__ == "__main__":

    program = Main()

    program.audio_option()
    program.neural_option()

    print("You will help this software improve its mood classification ability by putting in your own songs!")

    program.convertToWAV()
    program.model_predict()
    program.improvement()

    for i in range(0, 10):
        try:
            os.remove("../temp/song_output" + str(i) + ".png")
        except FileNotFoundError:
            continue

    print("Thank you for using this program! We will see you again.")
