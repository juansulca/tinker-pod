from displayio import Group
from adafruit_display_shapes.line import Line
from core import SCREEN_WIDTH
from random import randint
from base_app import App
from adafruit_ticks import ticks_ms, ticks_diff

LINE_COLOR = 0xDDDDDD

class Tiling(App):
  """
  Generative Art applicaiton
  """
  def __init__(self, root):
    # setup application UI
    self.splash = Group()
    root.append(self.splash)
    # set current division level
    self.n = 6

  def tiling(self, l: int):
    """
    Recursive tiling function
    l: int - level of division
    """
    # calculate size of the tiles
    size = SCREEN_WIDTH // l
    # for every tile on the screen
    for i in range(l):
      for j in range(l):
        # calculate top left corner of the tile
        x = i * size
        y = j * size
        # 50% chance of each option
        if randint(0, 1) > 0:
          # draw line top-left to bottom-right
          self.splash.append(Line(x, y, x + size, y + size, color=LINE_COLOR))
        else:
          # draw line top-right to bottom-left
          self.splash.append(Line(x, y + size, x + size, y, color=LINE_COLOR))

  def clear(self):
    """
    Clear screen and dealocate memory
    """
    # reverse all the lines on the screen
    while len(self.splash):
      # get each line object
      e = self.splash.pop()
      # delete the object form memory
      del e

  def cleanup(self, root):
    """
    Tear down the application
    """
    root.remove(self.splash)

  def draw(self):
    """
    Clean and Update the screen with the new tiling pattern
    """
    # clear screen
    self.clear()
    # call the algorithm to generate the tiles
    self.tiling(self.n)

  def run(self, btn_y, btn_x, btn_b, btn_a):
    # program loop
    last_update = ticks_ms()
    while True:
      now = ticks_ms()
      # update the screen every 200ms
      if ticks_diff(now, last_update) >= 200:
        if not btn_y.value:
          # Regenerate pattern with the same level
          self.draw()

        if not btn_x.value:
          # Increment cyclically the level of division
          # between 1 and 10, wrap around to 1
          self.n = ((self.n + 1) % 10) + 1
          # update the screen content
          self.draw()

        if not btn_a.value:
          # Decrease the level of division if it is greather than 1
          # never go bellow one
          self.n = (self.n - 1) if self.n > 1 else self.n
          # update the screen content
          self.draw()

        if not btn_b.value:
          # Exit the application
          return
        last_update = now
