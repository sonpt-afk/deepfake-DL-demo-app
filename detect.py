from tensorflow.keras.utils import img_to_array
from keras.models import load_model
import numpy as np
import pickle
import cv2
from tensorflow.keras.applications import DenseNet121
import tensorflow as tf
import time

class NoFaceDetectedException(Exception):
    pass

def detect(imgpath):
    start_time = time.time()
    print(imgpath)
  
    # Load file trọng số đã đào tạo trên Google Colab
    model = tf.keras.models.load_model('./fakevsreal_weights.keras')
  
    labels = ['real', 'fake']

    image = cv2.imread(imgpath)
    image = cv2.resize(image, (128, 128))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        raise NoFaceDetectedException("No face detected in the image")
    
    # Converting it to numpy array and expanding dimensions
    image = np.expand_dims(image, 0)
    
    # Predicting the label
    predictions = model.predict(image)
    print("predictions",predictions)
    # Extracting the label with maximum probability
    label = labels[np.argmax(predictions[0])]
    print("label",label)
    
    # Calculating the probability
    probab = float(round(predictions[0][np.argmax(predictions[0])]*100, 2))

    detection_time = time.time() - start_time

    return {"label": label,
     "probability": probab,
    "detection_time": detection_time,
    }

if __name__ == '__main__':
    detect()