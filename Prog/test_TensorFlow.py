from __future__ import absolute_import, division, print_function
import os
import time
import pathlib
import random
import tensorflow as tf

tf.enable_eager_execution()
AUTOTUNE = tf.data.experimental.AUTOTUNE


print("############ Charger le chemain de toutes les images")
#data_root = os.getcwd() + "/Image"
data_root = tf.keras.utils.get_file('flower_photos','https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz', untar=True)
data_root = pathlib.Path(data_root)

all_image_paths = [str(path) for path in list(data_root.glob('*/*'))]
random.shuffle(all_image_paths)
image_count = len(all_image_paths)
print("image_count =", image_count)


print("\n############ Determine the label for each image")
def caption_image(image_path):
    image_rel = pathlib.Path(image_path).relative_to(data_root)
    return str(image_rel)

label_names = sorted(item.name for item in data_root.glob('*/') if item.is_dir())
print("label_names =", label_names)

label_to_index = dict((name, index) for index,name in enumerate(label_names))
print("label_to_index =", label_to_index)

all_image_labels = [label_to_index[pathlib.Path(path).parent.name] for path in all_image_paths]


print("\n############ Load and format the images")
def preprocess_image(image):
  image = tf.image.decode_jpeg(image, channels=3)
  image = tf.image.resize_images(image, [192, 192])
  image /= 255.0  # normalize to [0,1] range
  return image

def load_and_preprocess_image(path):
  image = tf.read_file(path)
  return preprocess_image(image)

import matplotlib.pyplot as plt

img_path = all_image_paths[0]
label = all_image_labels[0]

plt.imshow(load_and_preprocess_image(img_path))
plt.grid(False)
plt.xlabel(caption_image(img_path))
plt.title(label_names[label].title())
plt.show()


print("\n############ A dataset of images")
path_ds = tf.data.Dataset.from_tensor_slices(all_image_paths)

print('shape: ', repr(path_ds.output_shapes))
print('type: ', path_ds.output_types)
print()
print(path_ds)

image_ds = path_ds.map(load_and_preprocess_image, num_parallel_calls=AUTOTUNE)

plt.figure(figsize=(8,8))
for n,image in enumerate(image_ds.take(4)):
  plt.subplot(2,2,n+1)
  plt.imshow(image)
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])
  plt.xlabel(caption_image(all_image_paths[n]))

plt.show()


print("\n############ A dataset of (image, label) pairs")
label_ds = tf.data.Dataset.from_tensor_slices(tf.cast(all_image_labels, tf.int64))

image_label_ds = tf.data.Dataset.zip((image_ds, label_ds))

print('image shape: ', image_label_ds.output_shapes[0])
print('label shape: ', image_label_ds.output_shapes[1])
print('types: ', image_label_ds.output_types)
print()
print(image_label_ds)

ds = tf.data.Dataset.from_tensor_slices((all_image_paths, all_image_labels))

# The tuples are unpacked into the positional arguments of the mapped function 
def load_and_preprocess_from_path_label(path, label):
  return load_and_preprocess_image(path), label

image_label_ds = ds.map(load_and_preprocess_from_path_label)
print(image_label_ds)


print("\n############ Basic methods for training")
BATCH_SIZE = 32

# Setting a shuffle buffer size as large as the dataset ensures that the data is
# completely shuffled.
ds = image_label_ds.shuffle(buffer_size=image_count)
ds = ds.repeat()
ds = ds.batch(BATCH_SIZE)
# `prefetch` lets the dataset fetch batches, in the background while the model is training.
ds = ds.prefetch(buffer_size=AUTOTUNE)
print(ds)

ds = image_label_ds.apply(tf.data.experimental.shuffle_and_repeat(buffer_size=image_count))
ds = ds.batch(BATCH_SIZE)
ds = ds.prefetch(buffer_size=AUTOTUNE)
print(ds)


print("\n############ Pipe the dataset to a model")
mobile_net = tf.keras.applications.MobileNetV2(input_shape=(192, 192, 3), include_top=False)
mobile_net.trainable=False

def change_range(image, label):
  return 2*image-1, label

keras_ds = ds.map(change_range)

# The dataset may take a few seconds to start, as it fills its shuffle buffer.
image_batch, label_batch = next(iter(keras_ds))

feature_map_batch = mobile_net(image_batch)
print(feature_map_batch.shape)

model = tf.keras.Sequential([
  mobile_net,
  tf.keras.layers.GlobalAveragePooling2D(),
  tf.keras.layers.Dense(len(label_names))
])

logit_batch = model(image_batch).numpy()

print("min logit:", logit_batch.min())
print("max logit:", logit_batch.max())
print()

print("Shape:", logit_batch.shape)

model.compile(optimizer=tf.train.AdamOptimizer(), 
              loss=tf.keras.losses.sparse_categorical_crossentropy,
              metrics=["accuracy"])

len(model.trainable_variables) 
model.summary()

steps_per_epoch=tf.ceil(len(all_image_paths)/BATCH_SIZE).numpy()
print(steps_per_epoch)

model.fit(ds, epochs=1, steps_per_epoch=3)


print("############ Performance")
def timeit(ds, batches=2*steps_per_epoch+1):
  overall_start = time.time()
  # Fetch a single batch to prime the pipeline (fill the shuffle buffer),
  # before starting the timer
  it = iter(ds.take(batches+1))
  next(it)

  start = time.time()
  for i,(images,labels) in enumerate(it):
    if i%10 == 0:
      print('.',end='')
  print()
  end = time.time()

  duration = end-start
  print("{} batches: {} s".format(batches, duration))
  print("{:0.5f} Images/s".format(BATCH_SIZE*batches/duration))
  print("Total time: {}s".format(end-overall_start))

ds = image_label_ds.apply(tf.data.experimental.shuffle_and_repeat(buffer_size=image_count))
ds = ds.batch(BATCH_SIZE).prefetch(buffer_size=AUTOTUNE)
print(ds)

timeit(ds)


print("############ Cache")
ds = image_label_ds.cache()
ds = ds.apply(tf.data.experimental.shuffle_and_repeat(buffer_size=image_count))
ds = ds.batch(BATCH_SIZE).prefetch(buffer_size=AUTOTUNE)
print(ds)

timeit(ds)
timeit(ds)
timeit(ds)


print("############ TFRecord File")
image_ds = tf.data.Dataset.from_tensor_slices(all_image_paths).map(tf.read_file)
tfrec = tf.data.experimental.TFRecordWriter('images.tfrec')
tfrec.write(image_ds)

image_ds = tf.data.TFRecordDataset('images.tfrec').map(preprocess_image)

ds = tf.data.Dataset.zip((image_ds, label_ds))
ds = ds.apply(tf.data.experimental.shuffle_and_repeat(buffer_size=image_count))
ds = ds.batch(BATCH_SIZE).prefetch(AUTOTUNE)
print(ds)

timeit(ds)

paths_ds = tf.data.Dataset.from_tensor_slices(all_image_paths)
image_ds = paths_ds.map(load_and_preprocess_image)
print(image_ds)

ds = image_ds.map(tf.serialize_tensor)
print(ds)

tfrec = tf.data.experimental.TFRecordWriter('images.tfrec')
tfrec.write(ds)

RESTORE_TYPE = image_ds.output_types
RESTORE_SHAPE = image_ds.output_shapes

ds = tf.data.TFRecordDataset('images.tfrec')

def parse(x):
  result = tf.parse_tensor(x, out_type=RESTORE_TYPE)
  result = tf.reshape(result, RESTORE_SHAPE)
  return result

ds = ds.map(parse, num_parallel_calls=AUTOTUNE)
print(ds)

ds = tf.data.Dataset.zip((ds, label_ds))
ds = ds.apply(tf.data.experimental.shuffle_and_repeat(buffer_size=image_count))
ds=ds.batch(BATCH_SIZE).prefetch(AUTOTUNE)
print(ds)

timeit(ds)


time.sleep(100000)