# Source : https://www.tensorflow.org/tutorials/images/hub_with_keras
from __future__ import absolute_import, division, print_function
import os
import matplotlib.pylab as plt

import tensorflow as tf
import tensorflow_hub as hub

import numpy as np

class MyModel:

    def __init__(self, name=""):
        self.model_name = name
        self.model = None
        self.data_root = None
        self.train_generator = None
        self.valid_generator = None
        self.IMAGE_SIZE = [224, 224]
        self.feature_extractor_url = None
        self.sess = tf.keras.backend.get_session()

    def set_feature_extractor(self, url):
        self.feature_extractor_url = url
        self.IMAGE_SIZE = hub.get_expected_image_size(hub.Module(url))

    def set_name(self):
        while len(self.model_name) < 3:
            self.model_name = input("model_name = ")
        if self.model_name == "auto":
            self.model_name = self.data_root[self.data_root.rfind('\\') + 1:-7]
            self.model_name += "V{}_".format(self.feature_extractor_url[self.feature_extractor_url.find("_v") + 2])

    def load_dataset(self, path=None):
        init = tf.global_variables_initializer()
        self.sess.run(init)

        print(" - Dataset - ")
        self.data_root = path

        train_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./ 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        self.train_generator = train_generator.flow_from_directory(self.data_root+"\\train", target_size=self.IMAGE_SIZE)

        valid_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./ 255)
        self.valid_generator = valid_generator.flow_from_directory(self.data_root+"\\valid", target_size=self.IMAGE_SIZE)

    def init_model(self):
        file = "saved_models/model_" + self.model_name + ".h5"
        if os.path.isfile(file) :
            print(" - Load the model - ")
            init = tf.global_variables_initializer()
            self.sess.run(init)

            self.model = tf.keras.models.load_model(file)
            self.model.summary()
        else:
            self.download_model()
            self.evaluate_model()
            self.save_model()

    def download_model(self):
        init = tf.global_variables_initializer()
        self.sess.run(init)

        print(" -----  Simple transfer learning  ----- ")
        print(" - Download the headless model - ")
        feature_extractor_url = self.feature_extractor_url

        def feature_extractor(x):
            feature_extractor_module = hub.Module(feature_extractor_url)
            return feature_extractor_module(x)


        [image_batch, label_batch] = self.train_generator[0]
        print("Image batch shape: ", image_batch.shape)
        print("Labe batch shape: ", label_batch.shape)

        features_extractor_layer = tf.keras.layers.Lambda(feature_extractor, input_shape=self.IMAGE_SIZE + [3])
        features_extractor_layer.trainable = False

        print(" - Attach a classification head - ")
        self.model = tf.keras.Sequential([
            features_extractor_layer,
            tf.keras.layers.Dense(self.train_generator.num_classes, activation='softmax')
        ])
        self.model.summary()

        init = tf.global_variables_initializer()
        self.sess.run(init)

        print(" - Train the model - ")
        self.model.compile(
            optimizer=tf.train.AdamOptimizer(),
            loss='categorical_crossentropy',
            metrics=['accuracy'])

        class CollectBatchStats(tf.keras.callbacks.Callback):
            def __init__(self):
                self.batch_losses = []
                self.batch_acc = []

            def on_batch_end(self, batch, logs=None):
                self.batch_losses.append(logs['loss'])
                self.batch_acc.append(logs['acc'])

        steps_per_epoch = self.train_generator.samples // self.train_generator.batch_size
        batch_stats = CollectBatchStats()

        self.model.fit((item for item in self.train_generator), epochs=1,
                  steps_per_epoch=steps_per_epoch,
                  callbacks=[batch_stats])

        if input(" - Show courbe - (o = True)").lower() == 'o':
            plt.figure()
            plt.ylabel("Loss")
            plt.xlabel("Training Steps")
            plt.ylim([0, 2])
            plt.plot(batch_stats.batch_losses)
            plt.show()

            plt.figure()
            plt.ylabel("Accuracy")
            plt.xlabel("Training Steps")
            plt.ylim([0, 1])
            plt.plot(batch_stats.batch_acc)
            plt.show()

    def check_predictions(self):
        init = tf.global_variables_initializer()
        self.sess.run(init)

        print(" - Check the predictions - ")
        label_names = sorted(self.train_generator.class_indices.items(), key=lambda pair: pair[1])
        label_names = np.array([key.title() for key, value in label_names])
        print(label_names)

        image_batch = self.train_generator[0][0]
        result_batch = self.model.predict(image_batch)
        labels_batch = label_names[np.argmax(result_batch, axis=-1)]
        print(labels_batch)

        if input(" - Show img - (o = True)").lower() == 'o':
            plt.figure(figsize=(10, 9))
            for n in range(30):
                plt.subplot(6, 5, n + 1)
                plt.imshow(image_batch[n])
                plt.title(labels_batch[n])
                plt.axis('off')
            _ = plt.suptitle("Model predictions")
            plt.show()

    def save_model(self):
        print(" -----  Export your model  ----- ")
        path = "saved_models/model_{}.h5".format(self.model_name)
        print(path)
        self.model.save(path)
        #export_path = tf.contrib.saved_model.save_keras_model(self.model, ".\\saved_models")
        #print(export_path)

    def evaluate_model(self):
        loss, acc = self.model.evaluate(self.valid_generator)
        print("Untrained model, accuracy: {:5.2f}%".format(100 * acc))
        if self.model_name[-1] == "_":
            self.model_name += str(int(10000*acc))

    def set_feature_extractor(self, url):
        self.feature_extractor_url = url
        self.IMAGE_SIZE = hub.get_expected_image_size(hub.Module(url))



if __name__ == "__main__":
    print(" -----  Setup  ----- ")
    tf.logging.set_verbosity(tf.logging.ERROR)

    m = MyModel()
    url_layer = ""
    while not url_layer.startswith("https://"):
        url_layer = input("feature_vector = ")
        if url_layer == "3":
            url_layer = "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/3"
        elif url_layer == "2":
            url_layer = "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/2"
    print(url_layer)
    m.set_feature_extractor(url_layer)

    path_photos = os.getcwd() + "\\dataset\\{}_photos"
    name_path = ""
    while not os.path.isdir(path_photos.format(name_path)):
        name_path = input("name_path = ?_photos  :  ")
    print(path_photos.format(name_path))
    m.load_dataset(path_photos.format(name_path))

    m.set_name()

    m.init_model()
    m.check_predictions()