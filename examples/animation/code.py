"""
Hello animation example
================================================================================

Sketch to move elements on the screen.

* Author(s): Juan Sulca

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit CircuitPython SSD1327 driver:
  https://github.com/adafruit/Adafruit_CircuitPython_SSD1327
* Adafruit CircuitPython Display Text library:
  https://github.com/adafruit/Adafruit_CircuitPython_Display_Shapes
"""

import board
import displayio
import adafruit_ssd1327
from adafruit_display_shapes.rect import Rect
import time

WIDTH = 128
HEIGHT = 128

# display setup
displayio.release_displays()
# use the integrated I2C STEMMA connector
i2c = board.STEMMA_I2C()
# match the device address, usually maked on the screen PCB
display_bus = displayio.I2CDisplay(i2c, device_address=0x3D)
# create the display controller
display = adafruit_ssd1327.SSD1327(display_bus, width=WIDTH, height=HEIGHT)
# set parent view for display
splash = displayio.Group()
display.root_group = splash

# store the velocity of the ball
velocity_x = 1
velocity_y = 1
# create a 3x3 rectangle, positioned at origin: 0,0
ball = Rect(0, 0, 3, 3, fill=0xFFFFFF)
#display the rectangle on the screen
splash.append(ball)

while True:
  # update the ball position
  ball.x += velocity_x
  ball.y += velocity_y

  # if the ball reaches the horizontal screen edge
  if ball.x > WIDTH - 3 or ball.x < 0:
    # reverse the x velocity
    velocity_x = -velocity_x

    # if the ball reaches the vertical screen edge
  if ball.y > HEIGHT - 3 or ball.y < 0:
    # reverse the y velocity
    velocity_y = -velocity_y

  # wait 0.1 seconds
  time.sleep(0.1)
