import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import adafruit_rgb_display.st7789 as st7789

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

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

image = Image.open("candle-3.jpg")
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Display image.
disp.image(image)


# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

#Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

def resizeCandle(img, h):
    
    counter = 0;
    # clear image
    draw.rectangle((0, 0, 240, 135), outline=0, fill=120)
    
    #img = img.copy()
    #img.paste(img, (0, h // 2))
    
   # img = img.transform(img.size, Image.EXTENT, (0, h, 0, 0))
    img = img.resize((width, h))
    
   # img = img.crop((10, 20, 20, 20))
    #img.filter(ImageFilter.MinFilter)
    disp.image(img)

while True:
    if buttonB.value and not buttonA.value:  # just button A pressed
        resizeCandle(image, 240)
    if buttonA.value and not buttonB.value:
        resizeCandle(image, 80)
    time.sleep(0.1)
