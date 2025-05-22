import os
import cv2
import numpy as np
import tensorflow as tf

from keras.models import load_model

# ------------------------------
# TensorFlow graph for TF 1.x
graph = tf.compat.v1.get_default_graph()

# Load model globally (only once)
model_path = r"C:\Users\Fatema Hana\PycharmProjects\eyecancer\eyecancer\myapp\model1.h5"
model = load_model(model_path)


# ------------------------------
def read_dataset1(path):
    data_list = []
    file_path = os.path.join(path)

    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"[ERROR] Image not found: {file_path}")

    res = cv2.resize(img, (48, 48), interpolation=cv2.INTER_CUBIC)
    data_list.append(res)
    return np.asarray(data_list, dtype=np.float32)


def predict(fn):
    dataset = read_dataset1(fn)
    dataset = dataset.reshape(dataset.shape[0], 48, 48, 1)
    dataset /= 255.0

    with graph.as_default():
        prediction = model.predict(dataset, verbose=0)
        predicted_class = np.argmax(prediction, axis=1)
        return predicted_class

