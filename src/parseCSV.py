import csv


class EmotionScoreDataset:
    """
    Class to hold all the information about the csv dataset.
    Parses the csv and stores it in a dict and a list for easy access.

    The dict is keyed by the TRACK_ID (first column of csv file).

    The format of the data is as follows:
    [song_name, artist_name, positive_score, neutral_score, negative_score] 
    """

    def __init__(self, filepath):
        """
        filepath -- path of the csv file.
        """
        self.songs_dict = {}
        self.songs_list = []
        self._parseCSV(filepath)

    def add_song(self, csv_row):
        scores = list(map(lambda x: int(x), str(csv_row[-1]).split("_")))
        self.songs_dict[csv_row[0]] = [
            csv_row[1],
            csv_row[2],
            scores[0],
            scores[1],
            scores[2]
        ]
        self.songs_list.append([
            csv_row[1],
            csv_row[2],
            scores[0],
            scores[1],
            scores[2]
        ])

    def _parseCSV(self, filepath):
        with open(filepath, 'r') as file:
            csvFile = csv.reader(file)
            for row in csvFile:
                self.add_song(row)

    def __repr__(self):
        """
        Used for getting a string representation of the class for printing to
        console for debug purposes. Prints the first 5 lines of the csv.
        """
        output = "CSVDataset({} rows, {} columns)\n".format(
            len(self.songs_list),
            len(self.songs_list[0])
        )

        for i in range(5):
            output += "{}\n".format(str(self.songs_list[i]))

        output += "...\n...\n..."
        return output


class YTDataset:
    def __init__(self, filepath):
        """
        filepath -- path of the csv file.
        """
        self.yt_links = {}
        self._parseCSV(filepath)

    def add_song(self, csv_row):
        self.yt_links[csv_row[0]] = csv_row[1:-1]

    def _parseCSV(self, filepath):
        with open(filepath, 'r') as file:
            csvFile = csv.reader(file)
            for row in csvFile:
                self.add_song(row)


# This is if we are running the file
# then just read the csv and print the first few lines
if __name__ == "__main__":
    print(YTDataset("../data/YouTubeURLs.csv").yt_links)
