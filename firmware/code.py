import board
import displayio
import terminalio
import adafruit_ssd1327
import random
import time
from math import ceil

monotonic_time = time.monotonic_ns()
random.seed(monotonic_time)

displayio.release_displays()
spi = board.SPI()

display_bus = displayio.FourWire(spi, command=board.D3, chip_select=board.D2, baudrate=1000000)

WIDTH = 128
HEIGHT = 128
TILE_SIZE = WIDTH // 4

display = adafruit_ssd1327.SSD1327(display_bus, width=WIDTH, height=HEIGHT)

splash = displayio.Group()
display.root_group = splash
bitmap = displayio.Bitmap(display.width, display.height, 2)
color_palette = displayio.Palette(2)
color_palette[0] = 0x000000  # White
color_palette[1] = 0xFFFFFF  # Black
bg_sprite = displayio.TileGrid(bitmap, pixel_shader=color_palette)

splash.append(bg_sprite)

def draw_line(x0, y0, x1, y1):
	if x0 == x1:
		for y in range(y0, y1):
			if y >= HEIGHT:
				return
			bitmap[x0, y] = 1
		return

	m = (y1 - y0) // (x1 - x0)
	c = (y0 * x1 - y1 * x0) // (x1 - x0)
	for x in range(x0, x1):
		y = m * x + c
		if y >= HEIGHT:
				return
		bitmap[x, y] = 1

def draw_rect(x, y, w, h = None):
	if h is None:
		h = w

	for i in range(w):
		for j in range(h):
			bitmap[x + i, y + j] = 1

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
	for j in range(WIDTH):
		for i in range(HEIGHT):
			bitmap[i, j] = 0

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
			bitmap[x + i, y + j] = 0

def type0Rect(n):
	(x, y) = get_xy(n)
	space = TILE_SIZE // 5
	for a in range(5):
		draw_line(x, y + a * space, x + a * space, y)
		if a % 2 == 0: continue
		for b in range(1, 6):
			draw_line(x, y + a*space + b, x + a*space + b, y)
	for a in range(6):
		draw_line(x + a*space, y + TILE_SIZE, x + TILE_SIZE, y + space * a)
		if a % 2 != 0: continue
		for b in range(1, space):
			draw_line(x + a*space + b, y + TILE_SIZE, x + TILE_SIZE, y + space * a + b)

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

# tiling(4)
type0Rect(0)
type1Rect(1)
type2Rect(2)
type3Rect(3)
type4Rect(4)
type7Rect(7)
type8Rect(8)

while(True):
	pass
