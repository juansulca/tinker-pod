from displayio import Group, Bitmap, Palette, TileGrid
from adafruit_ticks import ticks_ms, ticks_less, ticks_add
from adafruit_display_shapes.rect import Rect
import time

BRUSH_SIZE = 4
CANVAS_HEIGHT = 64
CANVAS_WIDTH = 64
_C_BLACK = 0x000000 # Color code for black
_C_WHITE = 0xDDDDDD # Color code for white
BLACK = 0 # palette index for black
WHITE = 1 # palette index for white

def make_canvas():
  """
  Create a 64x64 canvas with a 2-color palette
  returns: Tuple(Bitmap, TileGrid)
  """
  # create a 64x64 indexed image with 2 colors
  bitmap = Bitmap(CANVAS_WIDTH, CANVAS_HEIGHT, 2)
  # create a 2-color palette, order of colors is important!
  color_palette = Palette(2)
  color_palette[BLACK] = _C_BLACK
  color_palette[WHITE] = _C_WHITE
  # create a set of tiles that can be displayed on the screen
  bg_sprite = TileGrid(bitmap, pixel_shader=color_palette, width=64, height=64)
  # create a group to hold the sprite and scale it by 2 to cover 128x128 screen size
  canvas = Group(scale=2)
  canvas.append(bg_sprite)
  return bitmap, canvas

class Draw:
  def __init__(self, root):
    self.splash = Group()
    self.bitmap, self.canvas = make_canvas()
    # Create the visual maker for the pen
    self.marker = Rect(0, 0, BRUSH_SIZE, BRUSH_SIZE, outline=0x888888)
    # Store the position of the pen and set the pen state
    self.position = [0, 0]
    self.pen_down = True
    # Add the UI elements to the view
    self.splash.append(self.canvas)
    self.splash.append(self.marker)
    root.append(self.splash)

  def setPixel(self, x, y, color = 0):
    """
    Set a pixel on the canvas
    x: int
    y: int
    color: int
    """
    self.bitmap[x, y] = color

  def clear(self):
    """
    Clear the canvas setting it to black
    """
    for i in range(CANVAS_WIDTH):
      for j in range(CANVAS_HEIGHT):
        self.setPixel(i, j, BLACK)

  def run(self, btn_y, btn_x, btn_b, btn_a):
    """
    Execute the drawing application
    btn_y: Pin
    btn_x: Pin
    btn_b: Pin
    btn_a: Pin
    """
    # clear the canvas to set it black
    self.clear()
    # set the how long to wait before moving the pen
    deadline = ticks_add(ticks_ms(), 150)

    while True:
      now = ticks_ms()
      if ticks_less(deadline, now):
        # if all buttons are pressed, show the context menu
        if not (btn_y.value or btn_x.value or btn_b.value or btn_a.value):
          time.sleep(0.4)
          while True:
            # wait for user input
            if not btn_x.value:
              # Toggle pen down
              self.pen_down = not self.pen_down
              break
            if not btn_y.value:
              # close context menu
              break
            if not btn_a.value:
              # clear screen
              self.clear()
              break
            if not btn_b.value:
              # exit drawing application
              return
            time.sleep(0.1)


        if not btn_y.value:
          # move pen left
          self.position[0] -= 1 if self.position[0] > 0 else 0
        if not btn_x.value:
          # move pen right
          self.position[0] += 1 if self.position[0] < 63 else 0
        if not btn_b.value:
          # move pen up
          self.position[1] -= 1 if self.position[1] > 0 else 0
        if not btn_a.value:
          # move pen down
          self.position[1] += 1 if self.position[1] < 63 else 0

        # update the marker position and compensate for the 2x scale
        self.marker.x = self.position[0] * 2 - 1
        self.marker.y = self.position[1] * 2 - 1

        if self.pen_down:
          # draw on the canvas if the pen is down
          self.setPixel(self.position[0], self.position[1], WHITE)

        # update the deadline for the next update
        deadline = ticks_add(now, 150)

  def cleanup(self, root):
    """
    Tear down the drawing application
    root: Group
    """
    # remove the ui elements from the view
    root.remove(self.splash)
