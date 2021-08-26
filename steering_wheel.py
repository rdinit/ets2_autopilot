import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2


class SteeringWheel():
    def __init__(self):
        self.class_names = ['center', 'left', 'right', 'vleft', 'vright']
        self.model = keras.models.load_model('steering_model')

    def get(self, img, bbox=(440, 520, 990, 860)):
        #img = ImageGrab.grab(bbox=bbox)
        img = img.crop(box=bbox)
        
        test_image = np.array(img)
        cv2.imshow('wheel', test_image)
        cv2.waitKey(1)
        size = 40, 40
        
        test_image = cv2.resize(test_image, size, interpolation=cv2.INTER_LINEAR)
        size = 40, 40
        width, height = size
        

        test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2HSV)

        img2 = np.zeros((height,width,1), np.float)
        for i in range(height):
            for j in range(width):
                px = test_image[i,j].copy()
                img2[i, j] = [px[2]]
    
        img2 = tf.expand_dims(img2, 0) # Create a batch
        predictions = self.model.predict(img2)
        score = tf.nn.softmax(predictions[0])

        return self.class_names[np.argmax(score)]
