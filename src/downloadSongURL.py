import pafy
import time
from parseCSV import YTDataset, EmotionScoreDataset
import requests
import numpy as np
import sys

# code from https://gist.github.com/gaurav22verma/d1dd9cdb9527e1198244d66120afab7a#file-downloadsongfromurl-py-L2
# sample_URLs = ['wdPAIXBmcF0', 'FiiA9OSm5lc']

def getAudioFile(UID, filepath="./"):
    """
    Given a list of youtube UIDs for the same song
    this method tries to download the audio of the song until successful.

    UID -- ids of videos for the same song
    """
    for an_elt in UID:
        URL = an_elt.strip()
        try:
            video = pafy.new(URL, ydl_opts={'nocheckcertificate': True})
            # Check that the duration of the video is less than 10 minutes
            duration = video.duration.split(':')
            if int(duration[0]) == 0 and int(duration[1]) <= 10:
                bestaudio = video.getbestaudio()
                Title = str(video.title)
                bestaudio.download(filepath=filepath)
                return Title
            else:
                continue
        except Exception as e:
            print(e)
            time.sleep(21)
            continue


# def getURL(userInput):
#     MAXRESULTS = "1"
#     # TOKEN = INSERT API KEY HERE OR FUNCTION WILL NOT WORK
#     url = "https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=" + \
#         MAXRESULTS + "&q=" + userInput + "&key=" + TOKEN
#     x = requests.get(url)
#     y = x.json()['items'][0]['id']['videoId']
#     returnUrl = "https://www.youtube.com/watch?v=" + y
#     return returnUrl


def main(num_songs=10):
    # load csv datasets
    songUIDs = YTDataset("../data/YouTubeURLs.csv")
    emotionData = EmotionScoreDataset("../data/SongEmotionScore.csv")
    # get the id of the songs
    keys = list(songUIDs.yt_links.keys())
    
    
    for i in range(num_songs):
        key = keys[i]
        filepath = "../content/input_files/emotions/{}/"
        YTID = songUIDs.yt_links[key]       
        # set the correct folder for the song
        emotionScores = emotionData.songs_dict[key][2:]
        index = np.argmax(emotionScores)

        if index == 0:
            filepath = filepath.format("positive")
        elif index == 1:
            filepath = filepath.format("neutral")
        elif index == 2:
            filepath = filepath.format("negative")
        
        # download song into the correct folder 
        getAudioFile(YTID, filepath)

    # tested out to make sure getURL works
    # userInput = input("What do you want to search for: ")
    # result = getURL(str(userInput))
    # print(result)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(int(sys.argv[1]))
    else:
        main()
