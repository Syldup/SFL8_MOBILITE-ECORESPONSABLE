# Source : https://www.tensorflow.org/tutorials/images/hub_with_keras
from __future__ import absolute_import, division, print_function
import os
import matplotlib.pylab as plt

import tensorflow as tf
import tensorflow_hub as hub

import numpy as np
from model import MyModel

print(" -----  Setup  ----- ")
tf.logging.set_verbosity(tf.logging.ERROR)

m = MyModel()
m.load_dataset() # os.getcwd() + "\\dataset")
m.init_model()
m.check_predictions()
m.save_model()