# !/usr/bin/env python3
import numpy as np
import keras
import cv2 as cv
from imutils import paths
from keras.applications.inception_v3 import InceptionV3
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D, Flatten
from keras import backend as K


def extract_name(fp: str):
    return fp.split('/')[-2]


def extract_datasets(image_paths):
    X_binary = []
    Y_binary = []
    X_cat = []
    Y_cat = []
    for fp in image_paths:
        img = cv.imread(fp)
        name = extract_name(fp)
        img = cv.resize(img, (75, 75), interpolation=cv.INTER_AREA)
        if name == 'empty':
            Y_binary.append([1, 0])
            X_binary.append(img)

        else:
            Y_binary.append([0, 1])
            X_binary.append(img)
            ytemp = [0] * 9
            ytemp[int(name) - 1] = 1
            Y_cat.append(ytemp)
            X_cat.append(img)

    return np.array(X_binary), np.array(Y_binary), np.array(X_cat), np.array(Y_cat)


img_paths = list(paths.list_images('./images/dataset'))
X_b, Y_b, X_c, Y_c = extract_datasets(img_paths)

base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(75, 75, 3))

x = base_model.output
x = Flatten()(x)
# x = Dense(256, activation = 'relu')(x)
pred = Dense(9, activation='softmax', kernel_regularizer=keras.regularizers.l1_l2())(x)

model = Model(input=base_model.input, output=pred)
model.summary()

for layer in base_model.layers:
    layer.trainable = False
from keras.optimizers import RMSprop

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['acc'])

model.fit(x=X_c, y=Y_c, batch_size=32, epochs=10, validation_split=0.2)

for layer in model.layers[:249]:
    layer.trainable = False
for layer in model.layers[249:]:
    layer.trainable = True

from keras.optimizers import SGD

model.compile(optimizer=SGD(learning_rate=0.0001, momentum=0.9), loss='categorical_crossentropy', metrics=['acc'])
model.fit(x=X_c, y=Y_c, batch_size=32, epochs=10, validation_split=0.2)
