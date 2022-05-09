from keras.layers import (
    Reshape,
    Conv2D,
    MaxPool2D,
    Flatten,
    LSTM,
    BatchNormalization,
)
from keras.layers import Dropout, Dense, TimeDistributed
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten
from keras.layers import Dropout, Dense
from keras.models import Sequential
# from tensorflow.keras.applications import ResNet50
# from tensorflow.keras.models import Sequential
# from tensorflow.python.keras.layers import Dense, Flatten, GlobalAveragePooling2D, BatchNormalization
# from tensorflow.python.keras.applications.resnet50 import preprocess_input
# from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.python.keras.preprocessing.image import load_img, img_to_array

from models import resnet 



def create_model(input_shape):
    model = Sequential()
    # model.add(BatchNormalization(axis=1, input_shape=input_shape))
    # model.add(
    #     Conv2D(
    #         32,
    #         kernel_size=(3, 3),
    #         activation="relu",
    #         data_format="channels_last",
    #         input_shape=input_shape,
    #     )
    # )
    # model.add(
    #     Conv2D(
    #         64,
    #         kernel_size=(3, 3),
    #         activation="relu",
    #         data_format="channels_last",
    #         padding="same",
    #     )
    # )
    # model.add(MaxPool2D(pool_size=(2, 2)))
    # model.add(
    #     Conv2D(
    #         128,
    #         kernel_size=(3, 3),
    #         activation="relu",
    #         data_format="channels_last",
    #         padding="same",
    #     )
    # )
    # model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(resnet.ResNet34(input_shape))
    resize_shape = model.output_shape[2] * model.output_shape[3]
    model.add(Reshape((model.output_shape[1], resize_shape)))
    model.add(LSTM(128, return_sequences=True, input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(LSTM(128, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(128, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(128, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(BatchNormalization())
    model.add(TimeDistributed(Dense(64, activation="relu")))
    model.add(TimeDistributed(Dense(32, activation="relu")))
    model.add(BatchNormalization())
    model.add(TimeDistributed(Dense(16, activation="relu")))
    model.add(TimeDistributed(Dense(8, activation="relu")))
    model.add(Flatten())
    model.add(Dense(11, activation="softmax"))
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["acc"])

    return model
