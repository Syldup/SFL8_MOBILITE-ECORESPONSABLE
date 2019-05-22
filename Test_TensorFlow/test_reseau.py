# Source : https://www.tensorflow.org/tutorials/images/hub_with_keras
from __future__ import absolute_import, division, print_function
import os
import matplotlib.pylab as plt

import tensorflow as tf
import tensorflow_hub as hub

from tensorflow.keras import layers

print(" -----  Setup  ----- ")
tf.logging.set_verbosity(tf.logging.ERROR)

print(" - Dataset - ")
data_root = tf.keras.utils.get_file('flower_photos', 'https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz', untar=True)

image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1 / 255)
image_data = image_generator.flow_from_directory(str(data_root))

[image_batch, label_batch] = image_data[0]
print("Image batch shape: ", image_batch.shape)
print("Labe batch shape: ", label_batch.shape)
input("wait :")

print(" -----  An ImageNet classifier  ----- ")
print(" - Download the classifier - ")
classifier_url = "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/classification/2"  # @param {type:"string"}


def classifier(x):
    classifier_module = hub.Module(classifier_url)
    return classifier_module(x)


IMAGE_SIZE = hub.get_expected_image_size(hub.Module(classifier_url))

classifier_layer = layers.Lambda(classifier, input_shape=IMAGE_SIZE + [3])
classifier_model = tf.keras.Sequential([classifier_layer])
classifier_model.summary()

image_data = image_generator.flow_from_directory(str(data_root), target_size=IMAGE_SIZE)
for image_batch, label_batch in image_data:
    print("Image batch shape: ", image_batch.shape)
    print("Labe batch shape: ", label_batch.shape)
    break

import tensorflow.keras.backend as K

sess = K.get_session()
init = tf.global_variables_initializer()

sess.run(init)

if input(" - Run it on a single image - (o = True)") == 'o':
    import numpy as np
    import PIL.Image as Image

    grace_hopper = tf.keras.utils.get_file('image.jpg', 'https://storage.googleapis.com/download.tensorflow.org/example_images/grace_hopper.jpg')
    grace_hopper = Image.open(grace_hopper).resize(IMAGE_SIZE)
    # print(grace_hopper)

    grace_hopper = np.array(grace_hopper) / 255.0
    print(grace_hopper.shape)

    result = classifier_model.predict(grace_hopper[np.newaxis, ...])
    print(result.shape)

    predicted_class = np.argmax(result[0], axis=-1)
    print(predicted_class)
    input("wait :")

    print(" - Decode the predictions - ")
    labels_path = tf.keras.utils.get_file('ImageNetLabels.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
    imagenet_labels = np.array(open(labels_path).read().splitlines())

    plt.imshow(grace_hopper)
    plt.axis('off')
    predicted_class_name = imagenet_labels[predicted_class]
    _ = plt.title("Prediction: " + predicted_class_name)
    plt.show()

    result_batch = classifier_model.predict(image_batch)
    labels_batch = imagenet_labels[np.argmax(result_batch, axis=-1)]
    print(labels_batch)

    plt.figure(figsize=(10, 9))
    for n in range(30):
        plt.subplot(6, 5, n + 1)
        plt.imshow(image_batch[n])
        plt.title(labels_batch[n])
        plt.axis('off')
    _ = plt.suptitle("ImageNet predictions")
    plt.show()
    input("wait :")

print(" -----  Simple transfer learning  ----- ")
print(" - Download the headless model - ")
feature_extractor_url = "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/2"  # @param {type:"string"}


def feature_extractor(x):
    feature_extractor_module = hub.Module(feature_extractor_url)
    return feature_extractor_module(x)


IMAGE_SIZE = hub.get_expected_image_size(hub.Module(feature_extractor_url))

image_data = image_generator.flow_from_directory(str(data_root), target_size=IMAGE_SIZE)
for image_batch, label_batch in image_data:
    print("Image batch shape: ", image_batch.shape)
    print("Labe batch shape: ", label_batch.shape)
    break

features_extractor_layer = layers.Lambda(feature_extractor, input_shape=IMAGE_SIZE + [3])
features_extractor_layer.trainable = False
input("wait :")

print(" - Attach a classification head - ")
model = tf.keras.Sequential([
    features_extractor_layer,
    layers.Dense(image_data.num_classes, activation='softmax')
])
model.summary()

init = tf.global_variables_initializer()
sess.run(init)

result = model.predict(image_batch)
print(result.shape)
input("wait :")

print(" - Save checkpoints during training - ")
checkpoint_path = "saved_models/training_1/cp-{epoch:04d}.ckpt"

checkpoint_dir = os.path.dirname(checkpoint_path)
latest = tf.train.latest_checkpoint(checkpoint_dir)
print(latest)

cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, save_weights_only=True, period=5)

print(" - Train the model - ")
model.compile(
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


steps_per_epoch = image_data.samples // image_data.batch_size
batch_stats = CollectBatchStats()
model.fit((item for item in image_data), epochs=1,
          steps_per_epoch=steps_per_epoch,
          callbacks=[batch_stats, cp_callback])
"""
plt.figure()
plt.ylabel("Loss")
plt.xlabel("Training Steps")
plt.ylim([0,2])
plt.plot(batch_stats.batch_losses)
plt.show()

plt.figure()
plt.ylabel("Accuracy")
plt.xlabel("Training Steps")
plt.ylim([0,1])
plt.plot(batch_stats.batch_acc)
plt.show()"""
input("wait :")

print(" - Check the predictions - ")
label_names = sorted(image_data.class_indices.items(), key=lambda pair: pair[1])
label_names = np.array([key.title() for key, value in label_names])
print(label_names)

result_batch = model.predict(image_batch)

labels_batch = label_names[np.argmax(result_batch, axis=-1)]
print(labels_batch)
"""
plt.figure(figsize=(10,9))
for n in range(30):
  plt.subplot(6,5,n+1)
  plt.imshow(image_batch[n])
  plt.title(labels_batch[n])
  plt.axis('off')
_ = plt.suptitle("Model predictions")
plt.show()"""
input("wait :")

print(" -----  Export your model  ----- ")
model.save('saved_models/my_model.h5')
export_path = tf.contrib.saved_model.save_keras_model(model, ".\\saved_models")
print(export_path)
