# 0. import modules
import random
import time
import busio
import board
import time
from adafruit_bus_device.i2c_device import I2CDevice
from struct import pack, unpack


# 1. import helper functions from other labs
from helper_image import displayImage 
from helper_screen import displayText 
from helper_button import checkButton 

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
# register: screen
# register: microphone
# register: camera



# 2. load API and externals

# load: Teachable machines
# load: webserver 

# 3. build interaction flow

userCoughs = True
userInView = False
getInputTouchSensor = 255

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
    activateSpeechText("I will help you!")

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
                activateSpeechText("Welcome to the COVID-19 Detector")
                time.sleep(1)
                activateCheckFlow()
            time.sleep(0.1)

        except KeyboardInterrupt:
            # on control-c do...something? try commenting this out and running again? What might this do
            write_register(device, STATUS, 0)
            break


# Fire everything up

init()





