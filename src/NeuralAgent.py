import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras_preprocessing.image import img_to_array
from tensorflow.keras import layers, models
from tensorflow.python.keras import Input
from tensorflow.python.keras.models import model_from_json

"""
NeuralAgent.py contains a class called NeuralAgent that can train the music based on emotion

The code below is based and modified from the github source by Kunal Vaidya:
https://github.com/KunalVaidya99
https://towardsdatascience.com/music-genre-recognition-using-convolutional-neural-networks-cnn-part-1-212c6b93da76
"""


class NeuralAgent:

    def __init__(self, input_shape=(288, 432, 4), classes=None, train_directory='../content/split/spectrograms/train/',
                 test_directory='../content/split/spectrograms/test/'):
        train_data = ImageDataGenerator(rescale=1. / 255)
        self.train_generator = train_data.flow_from_directory(train_directory, target_size=(288, 432),
                                                              color_mode="rgba", class_mode='categorical',
                                                              batch_size=128)
        test_data = ImageDataGenerator(rescale=1. / 255)
        self.test_generator = test_data.flow_from_directory(test_directory, target_size=(288, 432), color_mode='rgba',
                                                            class_mode='categorical', batch_size=128)

        if classes is None:
            self.class_labels = ['negative', 'neutral', 'positive']
        self.input_shape = input_shape
        self.classes = len(self.class_labels)
        self.train_directory = train_directory
        self.model = None  # Initializes to none

    def get_class_labels(self):
        return self.class_labels

    """
    Convolutional neural network for audio training
    Code comes from the audio training tutorial from the following site:
    https://towardsdatascience.com/music-genre-recognition-using-convolutional-neural-networks-cnn-part-1-212c6b93da76
    
    The model has 5 convolutional layers and 1 dropout layer
    """

    def NeuralModel(self):
        model = models.Sequential()
        model.add(layers.Conv2D(8, kernel_size=(3, 3), strides=(1, 1),
                                activation='relu', input_shape=self.input_shape))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(16, kernel_size=(3, 3), strides=(1, 1),
                                activation='relu', input_shape=self.input_shape))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(32, kernel_size=(3, 3), strides=(1, 1),
                                activation='relu', input_shape=self.input_shape))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, kernel_size=(3, 3), strides=(1, 1),
                                activation='relu', input_shape=self.input_shape))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(128, kernel_size=(3, 3), strides=(1, 1),
                                activation='relu', input_shape=self.input_shape))
        model.add(layers.MaxPooling2D((2, 2)))

        model.add(layers.Flatten())
        model.add(layers.Dropout(rate=0.3))
        model.add(layers.Dense(self.classes, activation='softmax', name='fc' + str(self.classes)))
        model.add(Input(shape=self.input_shape))

        # Print the neural network information
        model.summary()

        return model

    """
    Save a model to json file and save weights as hdf5 file
    Code based and modified from https://machinelearningmastery.com/save-load-keras-deep-learning-models/
    """

    def save_model(self):
        model_json = self.model.to_json()
        with open("../saved_model/model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.model.save_weights("../saved_model/model.h5")
        print("Saved model to disk in saved_model folder")

    """
    Load a model to json file and load weights as hdf5 file
    Code based and modified from https://machinelearningmastery.com/save-load-keras-deep-learning-models/
    """

    def load_model(self):
        json_file = open('../saved_model/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        # load weights into new model
        self.model.load_weights("../saved_model/model.h5")
        print("Loaded model from disk")

    """
    Create the neural model 
    """

    def create_model(self):
        self.model = self.NeuralModel()

    def train(self):
        try:
            self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            self.model.fit(self.train_generator, epochs=80, validation_data=self.test_generator)

        except ValueError:
            print("There is no training data available! Please input some audio and generate the spectrogram!")

    def predict(self, image_data):
        image = img_to_array(image_data)
        image = np.reshape(image, (1, 288, 432, 4))
        prediction = self.model.predict(image / 255)
        prediction = prediction.reshape((3,))
        class_label = np.argmax(prediction)
        return class_label, prediction
