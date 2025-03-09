"""
Hello draw example
================================================================================

Sketch to set up a "canvas" and draw a rectangle on it.

* Author(s): Juan Sulca

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit CircuitPython SSD1327 driver:
  https://github.com/adafruit/Adafruit_CircuitPython_SSD1327
"""

import board
import displayio
import adafruit_ssd1327

WIDTH = 128
HEIGHT = 128

COLOR_BLACK = 0x000000 # Color code for black
COLOR_WHITE = 0xDDDDDD # Color code for white
BLACK = 0 # palette index for black
WHITE = 1 # palette index for white
CANVAS_WIDTH = 64
CANVAS_HEIGHT = 64

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

# creat the canvas
# create a 64x64 indexed image with 2 colors
bitmap = displayio.Bitmap(CANVAS_WIDTH, CANVAS_HEIGHT, 2)
# create a 2-color palette, order of colors is important!
color_palette = displayio.Palette(2)
color_palette[BLACK] = COLOR_BLACK
color_palette[WHITE] = COLOR_WHITE
# create a set of tiles that can be displayed on the screen
bg_sprite = displayio.TileGrid(bitmap, pixel_shader=color_palette, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
# create a group to hold the sprite and scale it by 2 to cover 128x128 screen size
canvas = displayio.Group(scale=2)
canvas.append(bg_sprite)

# add the canvas to the splash screen
splash.append(canvas)

# draw unfilled rectangle
# top side
for x in range(16, 32):
    bitmap[x, 16] = WHITE
# left side
for y in range(16, 32):
    bitmap[16, y] = WHITE
# bottom side
for x in range(16, 32):
    bitmap[x, 32] = WHITE
# right side
for y in range(16, 32):
    bitmap[32, y] = WHITE

while True:
    pass
