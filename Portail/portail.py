import keras
from PIL import Image, ImageOps
import numpy as np
import requests

model = keras.models.load_model('camera/keras_model.h5')

#URL_CAMERA = 'http://192.168.1.96:81/videostream.cgi?loginuse=admin&loginpas=6969'
URL_CAMERA = 'http://176.190.181.124:81/snapshot.cgi?user=admin&pwd=6969'
#cap = cv2.VideoCapture(URL_CAMERA)

labels = []
with open('camera/labels.txt','r') as f:
    lines = f.readlines()
for line in lines:
    label = (line.split(" ")[1]).replace('\n', "")
    labels.append(f'{label}')


def predict():
    img_data = requests.get(URL_CAMERA).content
    with open('static/output.jpg', 'wb') as handler:
        handler.write(img_data)

    np.set_printoptions(suppress=True)

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    image = Image.open('static/output.jpg')

    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data)
    i_pred = np.argmax(prediction[0])

    max_pred = prediction[0][i_pred]

    message = "Predicted: {} at {}%".format(labels[i_pred], int(max_pred * 100))
    return labels[i_pred],message, labels