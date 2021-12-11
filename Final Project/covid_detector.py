# 0. import modules
import random
import time

# 1. import helper functions from other labs
from helper_image import displayImage 
from helper_screen import displayText 
from helper_button import checkButton 

# 1. register hardware

# register: button 
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
    displayText(message)

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
    buttonStatus = checkButton()
    print(buttonStatus)

    activatePassiveMode()

    # if(buttonPressedOnce):
    #     activateCheckFlow()
    # elif(buttonNotPressed):
    #     activatePassiveMode()
    # else:
    #     activateScreen("Oops, something went wrong")

# Fire everything up

init()