# https://gist.github.com/fchollet/0830affa1f7f19fd47b06d4cf89ed44d

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, model_from_json
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from pathlib import Path
import tensorflow as tf
import matplotlib.pyplot as plt

def create_model():
    # dimensions of our images.
    img_width, img_height = 150, 150

    train_data_dir = 'data/train'
    validation_data_dir = 'data/validation'
    nb_train_samples = 2000
    nb_validation_samples = 800
    epochs = 50
    batch_size = 16

    if K.image_data_format() == 'channels_first':
        input_shape = (3, img_width, img_height)
    else:
        input_shape = (img_width, img_height, 3)

    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    #model.add(BatchNormalization())

    #model.add(Conv2D(32, (3, 3), activation='relu'))
    #model.add(MaxPooling2D(pool_size=(2, 2)))
    #model.add(BatchNormalization())

    #model.add(Conv2D(96, (3, 3), activation='relu'))
    #model.add(MaxPooling2D(pool_size=(2, 2)))
    #model.add(BatchNormalization())

    #model.add(Conv2D(64, (3, 3), activation='relu'))
    #model.add(MaxPooling2D(pool_size=(2, 2)))
    #model.add(BatchNormalization())
    #model.add(Dropout(0.2))

    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(5, activation='sigmoid')) # softmax

    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',
                  metrics={'output_a': 'accuracy'})

    # this is the augmentation configuration we will use for training
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        rotation_range=20,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    # this is the augmentation configuration we will use for testing:
    test_datagen = ImageDataGenerator(rescale=1. / 255)
    seed = 1

    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='categorical',
        seed=seed)

    validation_generator = test_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='categorical',
        seed=seed)

    model.fit_generator(
        train_generator,
        steps_per_epoch=nb_train_samples // batch_size,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=nb_validation_samples // batch_size)

    #loss, acc = model.evaluate(testImages, testLabels, verbose = 0)
    #print(acc * 100)

    return model


def affiche_image(path):
    image = tf.read_file(path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize_images(image, [192, 192])
    image /= 255.0

    plt.imshow(image)
    plt.grid(False)
    plt.show()

if __name__ == "__main__":

    name = input("Name : ")
    my_json = Path("%s.json" % name)
    my_h5 = Path("%s.h5" % name)

    if my_json.is_file() and my_h5.is_file():
        # load json and create model
        json_file = open(my_json, 'r')
        model_json = json_file.read()
        json_file.close()
        model = model_from_json(model_json)
        # load weights into new model
        model.load_weights(my_h5)

        model.compile(loss='categorical_crossentropy',
                      optimizer='rmsprop',
                      metrics={'output_a': 'accuracy'})

    else:
        model = create_model()
        model_json = model.to_json()
        with open(my_json, "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights(my_h5)

    txt = input("Flower file : ")

    while txt != "exit":
        path = Path('data/validation/%s' % txt)
        if path.is_file():
            affiche_image(path)
            prediction = model.predict(np.array(path))
            print(prediction)
        else:
            print("Introuvable")

        txt = input("Flower file : ")
