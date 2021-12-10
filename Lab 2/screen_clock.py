# Spark my fire (but not too close) - python + proximity sensor to give time when you can keep balance

import time
import subprocess
import digitalio
import board
import adafruit_rgb_display.st7789 as st7789
import board
import busio
import adafruit_apds9960.apds9960
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# credits to promiximty.py by the IDD team Fall 2021 in Lab 2 repo
# set sensor to right board port

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)

# enable sensor
sensor.enable_proximity = True
	
# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.height
width = disp.width
image = Image.new("RGB", (width, height))
rotation = 90


# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# get image from file
image = Image.open("candle_l.jpg")

# Switch on backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Draw a white filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(255, 255, 255))

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Define buttons inputs
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()


# Function to map one value range to the other (interpolate)
# source https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
# edited to accept integers only

def interpolate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = int(value - leftMin) / int(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


# function to resize image of candle based on dynamic value
def resizeCandle(img, h):
    
    #counter = 0;
    # clear image
    #draw.rectangle((0, 0, 240, 135), outline=0, fill=120)
    
    #img = img.copy()
    #img.paste(img, (0, h // 2))
    

    draw.rectangle((0, 0, width, height), fill=(255 - h, 0, 0), outline=0) # draw darking red background
    draw.rectangle((0, 0, width, h), fill=(h, h, h), outline=0) # draw rectangle

    img = img.resize((width, h))
    
    disp.image(img)

# Start loop
while True:
    prox = sensor.proximity # get proximity
    interProx = interpolate(prox, 0, 255, 1, 240) # set range initial sensor be in image dimensions
    
    if interProx > 210: # if high flame
        image = Image.open("candle_h.jpg")
        resizeCandle(image, int(interProx)) # convert float to int and pass to resize function
    else:
        image = Image.open("candle_l.jpg")
        resizeCandle(image, int(interProx)) # convert float to int and pass to resize function


    
    print(int(interProx))

        
    time.sleep(0.1)
