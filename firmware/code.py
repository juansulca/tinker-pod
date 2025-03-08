import board
import displayio
import terminalio
import adafruit_ssd1327
import random
import time
from math import ceil
from digitalio import DigitalInOut, Direction, Pull
from pong import Pong
from menu import Menu
from tiling import Tiling
from adafruit_display_shapes.line import Line

monotonic_time = time.monotonic_ns()
random.seed(monotonic_time)

displayio.release_displays()
i2c = board.STEMMA_I2C()

display_bus = displayio.I2CDisplay(i2c, device_address=0x3D)

WIDTH = 128
HEIGHT = 128
TILE_SIZE = WIDTH // 4
FPS = 60
FPS_DELAY = 1 / FPS

display = adafruit_ssd1327.SSD1327(display_bus, width=WIDTH, height=HEIGHT)

splash = displayio.Group()
display.root_group = splash
bitmap = displayio.Bitmap(display.width, display.height, 3)
bitmap.fill(1)
color_palette = displayio.Palette(3)
color_palette[0] = 0xDDDDDD  # White
color_palette[1] = 0x000000  # Black
bg_sprite = displayio.TileGrid(bitmap, pixel_shader=color_palette)

splash.append(bg_sprite)

btn_y = DigitalInOut(board.D1)
btn_y.direction = Direction.INPUT
btn_y.pull = Pull.UP

btn_x = DigitalInOut(board.D3)
btn_x.direction = Direction.INPUT
btn_x.pull = Pull.UP

btn_b = DigitalInOut(board.D0)
btn_b.direction = Direction.INPUT
btn_b.pull = Pull.UP

btn_a = DigitalInOut(board.D2)
btn_a.direction = Direction.INPUT
btn_a.pull = Pull.UP

def draw_line(x0, y0, x1, y1):
	if x0 == x1:
		for y in range(y0, y1+1):
			if y > HEIGHT - 1:
				return
			bitmap[x0, y] = 0
		return

	m = (y1 - y0) // (x1 - x0)
	c = (y0 * x1 - y1 * x0) // (x1 - x0)
	for x in range(x0, x1):
		y = m * x + c
		if y > HEIGHT - 1:
				return
		bitmap[x, y] = 0

def draw_rect(x, y, w, h = None):
	if h is None:
		h = w

	for i in range(w):
		for j in range(h):
			bitmap[x + i, y + j] = 0

def tiling(l):
	size = WIDTH // l
	for i in range(l):
		for j in range(l):
			x = i * size
			y = j * size
			if random.random() > 0.5:
				draw_line(x, y, x + size, y + size)
			else:
				draw_line(x, y + size, x + size, y)

def clear_screen():
	bitmap.fill(1)

def get_xy(n):
	_y = n // 4
	_x = n - (_y * 4)
	x = _x * TILE_SIZE
	y = _y * TILE_SIZE
	return (x, y)

def clear_quadrant(b):
	(x, y) = get_xy(b)
	for i in range(TILE_SIZE):
		for j in range(TILE_SIZE):
			bitmap[x + i, y + j] = 1

def type0Rect(n):
	(x, y) = get_xy(n)
	space = (TILE_SIZE - 1) // 5
	for a in range(5):
		draw_line(x, y + a * space, x + a * space, y)
		if a % 2 == 0: continue
		for b in range(1, 6):
			draw_line(x, y + a*space + b, x + a*space + b, y)
	for a in range(5):
		draw_line(x + a*space, y + TILE_SIZE - 1, x + TILE_SIZE - 1, y + space * a)
		if a % 2 != 0: continue
		for b in range(1, space):
			draw_line(x + a*space + b, y + TILE_SIZE - 1, x + TILE_SIZE - 1, y + space * a + b)

def type1Rect(n):
	(x, y) = get_xy(n)
	space = TILE_SIZE // 5
	for a in range(6):
		draw_line(x, y + a*space, x + a*space, y)

def type2Rect(n):
	(x, y) = get_xy(n)
	space = TILE_SIZE // 3
	for a in range(3):
		for b in range(3):
			if a % 2 != b % 2:
				draw_rect(x + space * a, y + space * b, space)

def type3Rect(n):
	(x, y) = get_xy(n)
	space = TILE_SIZE // 3
	draw_rect(x, y, space, TILE_SIZE)
	draw_rect(x + 2 * space, y, space, TILE_SIZE)

def type4Rect(n):
	(x, y) = get_xy(n)
	space = TILE_SIZE // 3
	for a in range(3):
		for b in range(3):
			if a % 2 or b % 2:
				offset_a = space * a
				offset_b = space * b
				draw_rect(x + offset_a, y + offset_b, space)

def type7Rect(n):
	(x, y) = get_xy(n)
	space = TILE_SIZE // 4
	draw_rect(x + space, y + space, space * 2)

def type8Rect(n):
	(x, y) = get_xy(n)
	draw_rect(x, y, TILE_SIZE)

def type9Rect(n):
	(x, y) = get_xy(n)
	space = TILE_SIZE // 4
	for a in range(space):
		draw_line(x, y + 3 * space + a, x + 3 * space + a, y)
		draw_line(x + a, y + TILE_SIZE - 1, x + TILE_SIZE - 1, y + a)

def type10Rect(n):
	(x, y) = get_xy(n)
	space = TILE_SIZE // 3
	for a in range(3):
		for b in range(3):
			if a % 2 == b % 2:
				draw_rect(x + space * a, y + space * b, space)

def type11Rect(n):
	(x, y) = get_xy(n)
	space = TILE_SIZE // 3
	draw_rect(x + space, y, space, TILE_SIZE)

def type12Rect(n):
	(x, y) = get_xy(n)
	space = TILE_SIZE // 4;
	for a in range(space):
		draw_line(x + a, y, x + TILE_SIZE, y + TILE_SIZE - a)
		draw_line(x, y + a, x + TILE_SIZE - a, y + TILE_SIZE)

def type13Rect(n):
	(x, y) = get_xy(n)
	space = TILE_SIZE // 6
	draw_rect(x+space, y + space, space, 4*space)
	draw_rect(x+4*space, y + space, space, 4*space)

def type14Rect(n):
	(x, y) = get_xy(n)
	space = TILE_SIZE // 6
	draw_rect(x+space, y + space, 4*space, space)
	draw_rect(x+space, y + 4*space, 4*space, space)

def type15Rect(n):
	(x, y) = get_xy(n)
	space = TILE_SIZE // 5
	draw_rect(x+space, y + space, 3*space, 2*space)

fns = [
	type0Rect,
	type1Rect,
	type2Rect,
	type3Rect,
	type4Rect,
	type7Rect,
	type8Rect,
	type9Rect,
	type10Rect,
	type11Rect,
	type12Rect,
	type13Rect,
	type14Rect,
	type15Rect
]

time.sleep(0.2)

t = Tiling(splash)
t.draw()

time.sleep(2)
t.clear()
t.cleanup(splash)

# type0Rect(0)
# type1Rect(1)
# type2Rect(2)
# type3Rect(3)
# type4Rect(4)
# type7Rect(7)
# type8Rect(8)
# type9Rect(9)
# type10Rect(10)
# type11Rect(11)
# type12Rect(12)
# type13Rect(13)
# type14Rect(6)
# type15Rect(15)

last_update_time = 0
now = 0

# pong = Pong(splash)
menu = Menu(splash)

while(True):
	now = time.monotonic()

	if last_update_time + FPS_DELAY <= now:

			# pong.update(btn_y, btn_x, btn_b, btn_a)
			menu.update(btn_y, btn_x, btn_b, btn_a)

			last_update_time = now
