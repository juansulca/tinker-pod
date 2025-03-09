"""
Hello button example
================================================================================

Sketch to setup a button and display the pressed state

* Author(s): Juan Sulca

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit CircuitPython SSD1327 driver:
  https://github.com/adafruit/Adafruit_CircuitPython_SSD1327
* Adafruit CircuitPython Display Text library:
  https://github.com/adafruit/Adafruit_CircuitPython_Display_Text
"""

import board
import displayio
import adafruit_ssd1327
from adafruit_display_text import label
from digitalio import DigitalInOut, Direction, Pull
import time
import terminalio

WIDTH = 128
HEIGHT = 128

font = terminalio.FONT

# display setup
displayio.release_displays()
# use the integrated I2C STEMMA connector
i2c = board.STEMMA_I2C()
# match the device address, usually maked on the PCB
display_bus = displayio.I2CDisplay(i2c, device_address=0x3D)
# create the display controller
display = adafruit_ssd1327.SSD1327(display_bus, width=WIDTH, height=HEIGHT)
# set parent view for display
splash = displayio.Group()
display.root_group = splash

# create a label
text = label.Label(font, text="P", color=0xFFFFFF, x=50, y=64, scale=3)
# append label to the parent view
splash.append(text)

# create a button
# create a digitla pin
button = DigitalInOut(board.D2)
# set the button as input
button.direction = Direction.INPUT
# enable internal pull up resistor
button.pull = Pull.UP

# empty loop
while True:
  # read button state
  # default button state is high (True) - pull up resistor
  # and low (False) when pressed
  is_pressed = not button.value

  if is_pressed:
    # scale the text by 3
    text.scale = 6
  else:
    # keep the text the original size
    text.scale = 1

  # wait for 0.1
  time.sleep(0.1)
