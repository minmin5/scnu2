import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing import image

model = keras.models.load_model('./resources/model/xception_v4_1_09_0.938.h5')
classes = ['nv', 'cancer', 'Purulent', 'Acne']

img = image.load_img('./resources/test/a.jpg', target_size=(150, 150))
img = image.img_to_array(img)
img = np.expand_dims(img, axis=0)
img = img/255.0
pred = model.predict(img)
pred = np.argmax(pred)
print(pred)
