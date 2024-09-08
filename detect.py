from tensorflow.keras.utils import img_to_array
from keras.models import load_model
import numpy as np
import pickle
import cv2
import tensorflow as tf

def detect(imgpath, outname):
    thresh = 0.5
    # Khởi chạy mô hình nhận diện khuôn mặt
    network = cv2.dnn.readNetFromCaffe('./DNN_face_detector/deploy.prototxt',
                                       './DNN_face_detector/res10_300x300_ssd_iter_140000.caffemodel')
    # Load mô hình đã đào tạo trên Google Colab
    model = tf.keras.models.load_model('fakevsreal_weights.keras')
    # Load nhãn đã được mã hoá (Label Encoder)
    le = pickle.loads(open('./le.pickle', "rb").read())

    # image path
    img = cv2.imread(imgpath)
    (h, w) = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    network.setInput(blob)
    detections = network.forward()
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            startX = max(0, startX)
            startY = max(0, startY)
            endX = min(w, endX)
            endY = min(h, endY)
            # Lấy vùng khuôn mặt
            face = img[startY:endY, startX:endX]
            if face.size == 0:
                print("Failed to extract face region")
                continue
            try:
                face = cv2.resize(face, (128, 128))
            except Exception as e:
                print(f"Error resizing face: {e}")
                continue
            face = face.astype("float") / 255.0
            face = img_to_array(face)
            face = np.expand_dims(face, axis=0)

            # Model sẽ dự đoán khuôn mặt là real/deepfake
            preds = model.predict(face)[0]
            print("model.predict value : " + str(model.predict(face)))
            j = np.argmax(preds)
            print("j value: " + str(j))
            label = le.classes_[j]
            print("Label is: " + str(label))

            # Vẽ box hình chữ nhật đóng khung khuôn mặt
            label_text = "{}: {:.4f}".format(label, preds[j])
            color = (0, 0, 255) if j == 0 else (0, 255, 0)  # Red for FAKE, Green for REAL
            cv2.putText(img, label_text, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            cv2.rectangle(img, (startX, startY), (endX, endY), color, 2)
    
    out = cv2.imwrite(f"./uploads/{outname}.jpg", img)

if __name__ == '__main__':
    detect()