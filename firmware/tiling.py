from displayio import Group, Bitmap, Palette, TileGrid
from adafruit_display_shapes.line import Line
from constants import SCREEN_WIDTH
import random

class Tiling:
  def __init__(self, root):
    print("starting tiling...")
    self.splash = Group()
    root.append(self.splash)
    self.n = 6
    self.end = False

  def tiling(self, l):
    size = SCREEN_WIDTH // l
    for i in range(l):
      for j in range(l):
        x = i * size
        y = j * size
        if random.random() > 0.5:
          self.splash.append(Line(x, y, x + size, y + size, color=0xDDDDDD))
        else:
          self.splash.append(Line(x, y + size, x + size, y, color=0xDDDDDD))
  
  def clear(self):
    while len(self.splash):
      e = self.splash.pop()
      del e

  def cleanup(self, root):
    root.remove(self.splash)

  def draw(self):
    self.clear()
    self.tiling(self.n)

  def update(self, btn_y, btn_x, btn_b, btn_a):
    if not btn_y.value:
      self.draw()
    
    if not btn_x.value:
      self.n = (self.n + 1) % 13
      self.n += 1 if self.n == 0 else 0
      self.draw()

    if not btn_a.value:
      self.n = (self.n - 1) if self.n > 1 else self.n
      self.draw()
    
    if not btn_b.value:
      self.end = True

  def has_ended(self):
    return self.end