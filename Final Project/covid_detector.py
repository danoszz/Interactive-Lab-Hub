# 0. import modules
import random
import time
import busio
import board
import time
from adafruit_bus_device.i2c_device import I2CDevice
import tensorflow.keras
import numpy as np
import cv2
import sys
import numpy as np
import tensorflow as tf

# 1. import helper functions from other labs

from helper_image import displayImage 
from helper_screen import displayText 

# 1. register hardware

# register: button 

DEVICE_ADDRESS = 0x6f  # device address of our button
STATUS = 0x03 # reguster for button status
AVAILIBLE = 0x1
BEEN_CLICKED = 0x2
IS_PRESSED = 0x4

# The follow is for I2C communications
i2c = busio.I2C(board.SCL, board.SDA)
device = I2CDevice(i2c, DEVICE_ADDRESS)

def write_register(dev, register, value, n_bytes=1):
    # Write a wregister number and value
    buf = bytearray(1 + n_bytes)
    buf[0] = register
    buf[1:] = value.to_bytes(n_bytes, 'little')
    with dev:
        dev.write(buf)

def read_register(dev, register, n_bytes=1):
    # write a register number then read back the value
    reg = register.to_bytes(1, 'little')
    buf = bytearray(n_bytes)
    with dev:
        dev.write_then_readinto(reg, buf)
    return int.from_bytes(buf, 'little')

# clear out LED lighting settings. For more info https://cdn.sparkfun.com/assets/learn_tutorials/1/1/0/8/Qwiic_Button_I2C_Register_Map.pdf
write_register(device, 0x1A, 1)
write_register(device, 0x1B, 0, 2)
write_register(device, 0x19, 0)


# register: touch sensor
# TODO: implement proximity sensor, instead of mock data

getInputTouchSensor = 255

# 2. load API and externals

# load: Teachable machines

# AUDIO

# Example from Tensorsflow python website
# source: https://www.tensorflow.org/lite/guide/inference#load_and_run_a_model_in_python

# TODO: connect to microphone

img = tf.placeholder(name="img", dtype=tf.float32, shape=(1, 64, 64, 3))
const = tf.constant([1., 2., 3.]) + tf.constant([1., 4., 4.])
val = img + const
out = tf.identity(val, name="out")

# Convert to TF Lite format
with tf.Session() as sess:
  converter = tf.lite.TFLiteConverter.from_session(sess, [img], [out])
  tflite_model = converter.convert()

# Load the TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_content=tflite_model)
interpreter.allocate_tensors()

# Continue to get tensors and so forth, as shown above...

# This example is directly copied from the Tensorflow examples provided from the Teachable Machine.

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

img = None
webCam = False
if(len(sys.argv)>1 and not sys.argv[-1]== "noWindow"):
   try:
      print("I'll try to read your image");
      img = cv2.imread(sys.argv[1])
      if img is None:
         print("Failed to load image file:", sys.argv[1])
   except:
      print("Failed to load the image are you sure that:", sys.argv[1],"is a path to an image?")
else:
   try:
      print("Trying to open the Webcam.")
      cap = cv2.VideoCapture(0)
      if cap is None or not cap.isOpened():
         raise("No camera")
      webCam = True
   except:
      print("Unable to access webcam.")


# Load the model
model = tensorflow.keras.models.load_model('/models/keras_model.h5')
# Load Labels:ds
labels=[]
f = open("labels.txt", "r")
for line in f.readlines():
    if(len(line)<1):
        continue
    labels.append(line.split(' ')[1].strip())


while(True):
    if webCam:
        ret, img = cap.read()

    rows, cols, channels = img.shape
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    size = (224, 224)
    img =  cv2.resize(img, size, interpolation = cv2.INTER_AREA)
    #turn the image into a numpy array
    image_array = np.asarray(img)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    print("I think its a:",labels[np.argmax(prediction)])

    if webCam:
        if sys.argv[-1] == "noWindow":
           cv2.imwrite('detected_out.jpg',img)
           continue
        cv2.imshow('detected (press q to quit)',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break
    else:
        break

cv2.imwrite('detected_out.jpg',img)
cv2.destroyAllWindows()

# load: webserver 
# TODO: feature removed due to complexity

#### This where the fun starts! ####

# 3. build interaction flow

# mock data for prototyping purposes

userCoughs = True
userInView = False or webCam


##### Helper functions: standalone functions to support main flow (and to be cleaner) #####

# helper function: activate screen and populate with text
def activateScreen(message):
    displayText(message, "")

# helper function: activate speech ability with text
def activateSpeech(message):
    print(message)

# helper function: activate speech and display text on screen
def activateSpeechText(message):
    activateScreen(message)
    activateSpeech(message)
    

# helper function: mock temperature check

def checkTemp():
    # check if sensor is activated, with threshold above 200
    if(getInputTouchSensor > 200):
        # user feedback: checking & loading
        activateSpeechText("Checking..")
        # mock loading
        time.sleep(random.uniform(0.2, 2.2))
        # mock temperature by randomizing between range (in celcius)
        return random.uniform(36.1, 39.1) 
    # if finger is not being pressed good enough
    elif(getInputTouchSensor < 200):
        activateSpeechText("Please press finger harder")
    else:
        activateSpeechText("Please put finger on scanner")

# helper function: mock probability COVID-19, i.e. based on past user data, patterns and new insights

def checkProb():
    # fancy math + old data / average, for now a random function
    return random.uniform(0, 1)

    
##### Flow functions: these indicate the main proceses #####

# function flow: check temperature of user
def activateCheckFlow():

    # welcome message
    activateScreen("I will help you!")

    # get first probability 
    probCovid = checkProb()

    # calculate probibility with each cough for more real experience
    if(userCoughs):
        probCovid = checkProb()
        return probCovid

    if(userCoughs and userInView and probCovid >= 0.5):
        activateSpeechText("We will do a quick temperate check, please put your finger on the scanner")

        # get fake temperature
        temp = checkTemp()

        if(temp >= 38):
           activateSpeechText("Your temperature is high, you might be infected with COVID-19, the staff is being notified")
           time.sleep(2)
           activateSpeechText("Please wear a mask and wash your hands until the staff comes")
           time.sleep(2)
           activateSpeechText("Please wear a mask and wash your hands until the staff comes")

        elif(temp < 38):
            activateSpeechText("All good, thanks!")

    elif(userCoughs and probCovid >= 0.5):
        activateSpeechText("Please stand infront of camera")
    elif(userCoughs and probCovid < 0.5):
        activateSpeechText("Nothing found, all good")
    else:
        activateSpeechText("Oops, something went wrong")


# function flow: passive mode of device

def activatePassiveMode():
    # display Image
    displayImage("assets/ui-splashscreen.jpg")



##### Intial Functions: start of the device#####

def init():
    activatePassiveMode()
    while True:
        try:
            # get the button status
            btn_status = read_register(device, STATUS)
        
            # if pressed activate flow
            if (btn_status&IS_PRESSED) != 0:
                # Welcome message
                activateScreen("Welcome to the COVID-19 Detector")
                time.sleep(1)
                activateCheckFlow()
            time.sleep(0.1)

        except KeyboardInterrupt:
            # on control-c do...something? try commenting this out and running again? What might this do
            write_register(device, STATUS, 0)
            break


# Fire everything up

init()





