# CSCI 357 Midterm Project

Bucknell University

Spring 2021

**Publication link: https://medium.com/bucknell-ai-cogsci/automated-emotion-recognition-in-songs-993ed84dbc21**

## Group members
* Christina Yu
* Swarup Dhar
* Hannah Shin
* Lawrence Li

## Group name: Hello Life! Can't Sleep

## Project description

In this project, we aimed to improve the mood classification of the music based on user given emotion using neural network training.
We are using the IMAC dataset for neural network training, which is currently available collection of audio features and metadata for a million contemporary popular music tracks.

IMAC dataset: https://gaurav22verma.github.io/IMAC_Dataset.html

We manually downloaded the songs using a python script stored in `src/downloadSongURL.py` with `data/YouTubeURLs.csv` from the IMAC dataset.
Then we use the emotion score from `data/SongEmotionScore.csv` to put the audio files into corresponding emotion class folder.
We phrase both csv files using `src/parseCSV.py` and manually downloaded all the songs from the corresponding links and put all of them in appropriate emotion class folder.
We put all the downloaded songs in `content/input_files/emotions/` in each emotion category. 

## Running the Project

### HTML Server

The `Server` folder contains files necessary to run the `flask` python server that provides a way for the user to interface with our back-end model.

In order to run the server, make sure you have the following packages installed:

```pip install librosa matplotlib numpy pydub shutil keras Keras-Preprocessing tensorflow tensorflow.keras ffmpeg ffprobe flask```

Finally to run the server, go **inside** the `Server` folder and run `python server.py`. Very important that you are inside the Server folder when you run the `server.py` file. See the [section on known issues](#known-issues) involving SSL certificates. 

### Backend Program

The backend program consisted of one terminal program that will run from command prompt.
All trained music in `wav` format is stored in `content/input_files/emotions/` folder with three folder indicating
three emotion classifications: `positive neutral negative`. All the audio files are first downloaded from the Youtube URL 
as described by the IMAC dataset we are using for this project.

The backend program is able to create or load a neural model for training. It can split train and test (validation) dataset.
It can also have the ability to predict the probability of each emotion class given the song.

**Instructions to run backend program**

1. Install the required packages:
   `librosa; matplotlib; numpy; pydub (AudioSegment); shutil; keras; keras.preprocessing; tensorflow;
   tensorflow.keras; ffmpeg; ffprobe`
   
2. `cd src` and run `python main.py` This is important you will need to run `main.py` inside the `src` directory.

3. The terminal will prompt whether the user want to delete all the spectrograms generated from the previous run.
Type `y` if you want to recreate all the spectrograms from the beginning.
   WARNING: This will remove all spectrograms including the one the user added in step 12. 
   Delete only if you want to reset and start from the beginning.

4. The terminal will prompt whether the user want to create spectrograms
for the audio files stored in `content/input_files/emotions/`. Type `y` only if
   you want to create all the spectrograms from the beginning. (Make sure you have deleted all the spectrograms generated from
   the previous run in step 3)
   
5. Now it will prompt whether the user want to split train and test data. Type `y` only
if you have recreated all the spectrograms from the beginning in step 4.
   
6. Now it will prompt whether the user want to create a new neural model or
load an existing neural model. Type `create` if you want to start with a new neural network for training.
   Type `load` if you have trained the model using this program before and saved it in the `saved_model` folder.

7. Now it will prompt whether the user want to train the music. Type `y` if you want to train all the audio files. Type `n` only
if you loaded the model in step 6 and wish to not train it again. 
   
8. If you choose to train the model in step 7, it will now begin to train the model in 80 epochs. It will take some time.
Now it will prompt user to save the model. WARNING: Choosing `y` will OVERWRITE the previously saved model.
   
9. Here comes the main part. The terminal will prompt user to enter the name of the song that they put inside the 
`your_music` folder. At this time the user's audio files will be automatically converted to wav format. When prompted, simply type
   the name of the audio file WITHOUT the file extension.
   
10. In the final part, the program will give a probability score for each 
emotion class. You can now decide whether this prediction is accurate or not.
    Type `y` for accurate prediction or `n` for inaccurate prediction.

11. If you typed `y` in step 10, the program is finished (and you are DONE). Otherwise,
go to step 12.
    
12. The terminal will prompt user to add the song to the training list. Type `y` for adding the song to the training list or `n` for not.

If you added the song to the training list, you WILL NOT need to recreate the spectrograms. You will only
need to retrain the data. Simply run the `main.py` again, load the model, and retrain the model to fit your preferences.

## Known Issues

You may encounter SSL certificate errors when trying to run either the server. Specifically, when the agent tries to download songs from YouTube URL your system might throw a SSL error. This may vary between operating systems and currently the one work around is to go to your python installation foldering and run the `Install Certificates.command` inside. So for example, if you are on Mac:

 - Head to `Application / Python (Version)` folder
 - Double-click the `Install Certificates.command` inside the Python installation folder.

This should fix any SSL certificates issues. 

### References

We based and modified the implementation from others:

1. https://towardsdatascience.com/music-genre-recognition-using-convolutional-neural-networks-cnn-part-1-212c6b93da76
2. https://towardsdatascience.com/music-genre-recognition-using-convolutional-neural-networks-part-2-f1cd2d64e983
3. https://machinelearningmastery.com/save-load-keras-deep-learning-models/
