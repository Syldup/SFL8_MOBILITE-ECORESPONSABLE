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
        if url.startswith("https://"):
            self.feature_extractor_url = url
            self.IMAGE_SIZE = hub.get_expected_image_size(hub.Module(url))

    def choice_feature_extractor(self, idx = -1):
        print(" - Feature Extractor - ")
        urls_layer = dict()
        urls_layer["inception_v3 - iV3"] = "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/3"
        urls_layer["mobilenet_v2 - mV2"] = "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/2"

        key = *urls_layer.keys(),
        for i, k in enumerate(key):
            print("{} - {} : {}".format(i, k, urls_layer[k]))

        while idx < 0 or idx >= len(key):
            idx = int(input("index_feature_vector = "))
        self.set_feature_extractor(urls_layer[key[idx]])
        if self.model_name.startswith("auto"):
            self.model_name += "_" + key[idx][key[idx].rfind(" - ")+3:]

    def load_dataset(self, path=None):
        init = tf.global_variables_initializer()
        self.sess.run(init)
        self.data_root = path

        train_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./ 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        self.train_generator = train_generator.flow_from_directory(self.data_root+"\\train", target_size=self.IMAGE_SIZE)

        valid_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./ 255)
        self.valid_generator = valid_generator.flow_from_directory(self.data_root+"\\valid", target_size=self.IMAGE_SIZE)

    def choice_dataset_path(self, idx = -1):
        print(" - Dataset - ")
        dataset_path = os.getcwd() + "\\dataset\\"
        if os.path.isdir(dataset_path):
            name_paths = [path for path in os.listdir(dataset_path) if os.path.isdir(dataset_path + path)]
            for i, v in enumerate(name_paths):
                print("{} - {}".format(i, v))

            while idx < 0 or idx >= len(name_paths):
                idx = int(input("index_dataset_path = "))

            self.load_dataset(dataset_path + name_paths[idx])
            if self.model_name.startswith("auto"):
                self.model_name += "_" + name_paths[idx]
        else:
            raise IOError("dataset dir is not find")

    def set_name(self, name):
        self.model_name = name

    def get_name(self):
        if self.model_name.startswith("auto_"):
            return self.model_name[5:]
        return self.model_name

    def init_model(self):
        models_path = os.getcwd() + "\\saved_models\\"
        if os.path.isdir(models_path):
            models_name = [path for path in os.listdir(models_path) if path.startswith("model_"+self.get_name()) and path.endswith(".h5")]
            if len(models_name) != 0:
                print("0 - new_model")
                for i, v in enumerate(models_name):
                    print("{} - {}".format(i + 1, v))

                idx = -1
                while idx < 0 or idx > len(models_name):
                    idx = int(input("index_model = "))

                if idx != 0:
                    print(" - Load the model - ")
                    init = tf.global_variables_initializer()
                    self.sess.run(init)

                    self.model = tf.keras.models.load_model(models_path + models_name[idx-1])
                    self.model.summary()
                    return None

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

        self.model.fit((item for item in self.train_generator), epochs=5,
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

    def predict(self):
        print(" - Run it on a single image - ")
        init = tf.global_variables_initializer()
        self.sess.run(init)

        from tkinter.filedialog import askdirectory
        img_dir = askdirectory() + "/"
        imgs = list()
        if os.path.isdir(img_dir):
            imgs_name = [path for path in os.listdir(img_dir) if  path[path.rfind("."):] in [".jpg", ".png", ".jfif", ".jpeg"]]
            for img_name in imgs_name:
                img = tf.keras.preprocessing.image.load_img(img_dir + img_name, target_size=(*self.IMAGE_SIZE, 3))
                img = np.array(img) / 255.0
                #img = np.expand_dims(img, axis=0)

                imgs.append(img)

        if len(imgs) != 0:
            result = self.model.predict(np.array(imgs))
            print(result)
            print(result.shape)
            label_names = sorted(self.train_generator.class_indices.items(), key=lambda pair: pair[1])
            label_names = np.array([key.title() for key, value in label_names])
            labels = label_names[np.argmax(result, axis=-1)]
            print(labels)
        else:
            print("No image")

    def save_model(self):
        print(" -----  Export your model  ----- ")
        path = "saved_models/model_{}.h5".format(self.get_name())
        print(path)
        self.model.save(path)
        #export_path = tf.contrib.saved_model.save_keras_model(self.model, ".\\saved_models")
        #print(export_path)

    def evaluate_model(self):
        loss, acc = self.model.evaluate(self.valid_generator)
        print("Untrained model, accuracy: {:5.2f}%".format(100 * acc))
        if self.model_name.startswith("auto"):
            self.model_name += "_" + str(int(10000*acc))


if __name__ == "__main__":
    print(" -----  Setup  ----- ")
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    m = MyModel("auto_")

    m.choice_feature_extractor(0)
    m.choice_dataset_path(1)

    m.init_model()
    m.check_predictions()
    while input("Simpel predicrtion : ") == "o":
        m.predict()
