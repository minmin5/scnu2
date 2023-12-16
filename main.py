# import RPi.GPIO as GPIO
# import time
from os import path
import sys
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
from PyQt5 import uic
import cv2
from picamera2 import Picamera2
import tensorflow as tf
import threading
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing import image

model = keras.models.load_model('./resources/model/xception_v4_1_09_0.938.h5')
classes = ['nv', 'cancer', 'Purulent', 'Acne']

picam = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AISCAKI')
        self.uiStack = QStackedWidget()
        self.setCentralWidget(self.uiStack)
        self.mainui = uic.loadUi('./resources/ui/mainscreen.ui')
        self.mainui.startbtn.clicked.connect(lambda: self.uiStack.setCurrentIndex(1))
        
        self.nextui = uic.loadUi('./resources/ui/next1.ui')
        self.nextui.pushButton.clicked.connect(lambda: self.uiStack.setCurrentIndex(2))
        self.nextui.pushButton_2.clicked.connect(lambda: self.uiStack.setCurrentIndex(1))
        
        self.cameraui = uic.loadUi('./resources/ui/camera.ui')
        def capcam():
            self.cam = False
            img = self.frame
            img = cv2.resize(img, (150, 150))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = img/255.0
            pred = model.predict(img)
            pred = np.argmax(pred)
            print(pred)
            
            
        self.cameraui.picbtn.clicked.connect(capcam)
        def lam():
            self.cam = False
            self.uiStack.setCurrentIndex(3)
        self.cameraui.picbtn_2.clicked.connect(lam)
        
        self.processui = uic.loadUi('./resources/ui/pro1.ui')
        self.normalresui = uic.loadUi('./resources/ui/normalcomplete.ui')
        self.acneresui = uic.loadUi('./resources/ui/acnecomplete.ui')
        self.cancerresui = uic.loadUi('./resources/ui/cancer.ui')
        
        self.uiStack.addWidget(self.mainui)
        self.uiStack.addWidget(self.nextui)
        self.uiStack.addWidget(self.cameraui)
        self.uiStack.addWidget(self.processui)
        self.uiStack.addWidget(self.normalresui)
        self.uiStack.addWidget(self.acneresui)
        self.uiStack.addWidget(self.cancerresui)
        
        # set first screen
        self.uiStack.setCurrentIndex(0)
        self.show()

    def run_camera(self):
        while self.cam:
            self.frame = picam2.get_frame()
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frame = cv2.flip(self.frame, 1)
            self.frame = cv2.resize(self.frame, (640, 480))
            self.frame = QImage(self.frame, 640, 480, QImage.Format_RGB888)
            self.cameraui.camera.setPixmap(QPixmap.fromImage(self.frame))
            self.cameraui.camera.setScaledContents(True)
            self.cameraui.camera.show()
    def camera(self):
        self.uiStack.setCurrentIndex(2)
        self.cam = True
        self.thrd = threading.Thread(target=self.run_camera)
        self.thrd.start()
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
    
    
    

# pins = (18, 19, 21) # 빨강은 18핀, 초록은 19핀, 파랑은 21핀 지정

# def led(pins, color, t):
#     RGBs = (
#         (1,1,1), # 하양색
#         (1,0,0), # 빨강색
#         (0,1,0), # 초록색
#         (0,0,1), # 파랑색
#         (0,1,1), # 청록색
#         (1,0,1), # 보라색
#         (1,1,0), # 노랑색
#     )

#     GPIO.setmode(GPIO.BOARD)

#     GPIO.setup(pins[0], GPIO.OUT)
#     GPIO.setup(pins[1], GPIO.OUT)
#     GPIO.setup(pins[2], GPIO.OUT)

#     GPIO.output(pins[0], RGBs[color][0])
#     GPIO.output(pins[1], RGBs[color][1])
#     GPIO.output(pins[2], RGBs[color][2])

#     time.sleep(t)

#     GPIO.cleanup(pins)

# led(pins, 4, 10) # 청록색으로 10초 동안 점등