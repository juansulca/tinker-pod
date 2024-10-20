from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
import terminalio
import time

font = terminalio.FONT

class Ball:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.velocity = (1, 0)
    self.r = 4
    self.circle = Rect(self.x, self.y, self.r, self.r, fill=0xDDDDDD, outline=0xDDDDDD)

    self.SCREEN_WIDTH = 128
    self.SCREEN_HEIGHT = 128

  def check_collisions(self, paddle_l, paddle_r):
    if self.x <= paddle_l.x + paddle_l.width and paddle_l.y <= self.y <= paddle_l.y + paddle_l.height:
      y_velocity = self.velocity[1] if paddle_l.velocity == 0 else paddle_l.velocity
      self.velocity = (-self.velocity[0], y_velocity)

    if self.x >= paddle_r.x - paddle_r.width and paddle_r.y <= self.y <= paddle_r.y + paddle_r.height:
      y_velocity = self.velocity[1] if paddle_r.velocity == 0 else paddle_r.velocity
      self.velocity = (-self.velocity[0], y_velocity)

  def update(self):
    self.x += self.velocity[0]
    self.y += self.velocity[1]

    # if self.x < 0 or self.x > self.SCREEN_WIDTH - (self.r * 2):
    #   self.velocity = (self.velocity[0] * -1, self.velocity[1])

    if self.y < 0 or self.y > self.SCREEN_HEIGHT - (self.r * 2):
      self.velocity = (self.velocity[0], self.velocity[1] * -1)

    self.circle.x = self.x
    self.circle.y = self.y

  def reset(self):
    self.x = 64
    self.y = 64
    self.velocity = (1, 0)


class Paddle:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.width = 4
    self.height = 24
    self.velocity = 0

    self.rect = Rect(self.x, self.y, self.width, self.height, fill=0x999999, outline=0x999999)

  def update(self, up, down):
    if up and self.y > 0:
      self.velocity = -1
    else:
      self.velocity = 0

    if down and self.y < 127 - self.height:
      self.velocity = 1

    if not up and not down:
      self.velocity = 0

    self.y += self.velocity
    self.rect.y = self.y

  def reset(self):
    self.y = 52

class Score:
  def __init__(self, x, y):
    self.p1 = 0
    self.p2 = 0

    self.label = label.Label(font, text=f"{self.p1} - {self.p2}", color=0xEEEEEE)
    self.label.x = x
    self.label.y = y

  def update(self, ball):
    added = False
    if ball.x <= 4:
      self.p2 += 1
      added = True
    if ball.x + ball.r >= 125:
      self.p1 += 1
      added = True

    if added:
      self.label.text = f"{self.p1} - {self.p2}"
      time.sleep(1)
      ball.reset()

  def reset(self):
    self.p1 = 0
    self.p2 = 0
    self.label.text = f"{self.p1} - {self.p2}"
