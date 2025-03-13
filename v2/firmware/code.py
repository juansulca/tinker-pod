import board
import random
import time
from displayio import OnDiskBitmap, Group, TileGrid
from menu import Menu
from core import make_button, display_setup
from adafruit_ticks import ticks_ms

# set seed for pseudo-random number generation
random.seed(ticks_ms())

# display setup
display = display_setup()
# set parent view for display
splash = Group()
display.root_group = splash

# button setup
btn_y = make_button(board.D1)
btn_x = make_button(board.D3)
btn_b = make_button(board.D0)
btn_a = make_button(board.D2)

# load the splash image from disk
bitmap_slash = OnDiskBitmap("/TP_splash.bmp")
# display the splash and position it in the screen
t_grid = TileGrid(bitmap_slash, pixel_shader=bitmap_slash.pixel_shader)
t_group = Group()
t_group.append(t_grid)
t_group.x = 16
t_group.y = 40
splash.append(t_group)

time.sleep(3)

# remove the splash screen and dealocate the memory
splash.remove(t_group)
del t_group
del t_grid
del bitmap_slash

# create the root application
menu = Menu(splash)

menu.run(btn_y, btn_x, btn_b, btn_a)
