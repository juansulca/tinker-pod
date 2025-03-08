from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
import terminalio
import time
from displayio import Group

font = terminalio.FONT

class Puck:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.velocity = (1, 0)
    self.r = 4
    self.sprite = Rect(self.x, self.y, self.r, self.r, fill=0xDDDDDD, outline=0xDDDDDD)

    self.SCREEN_WIDTH = 128
    self.SCREEN_HEIGHT = 128

  def check_collisions(self, paddle_l, paddle_r):
    if self.x <= paddle_l.x + paddle_l.width/2 and paddle_l.y <= self.y <= paddle_l.y + paddle_l.height:
      y_velocity = self.velocity[1] if paddle_l.velocity == 0 else paddle_l.velocity
      self.velocity = (-self.velocity[0], y_velocity)

    if self.x >= paddle_r.x - paddle_r.width/2 and paddle_r.y <= self.y <= paddle_r.y + paddle_r.height:
      y_velocity = self.velocity[1] if paddle_r.velocity == 0 else paddle_r.velocity
      self.velocity = (-self.velocity[0], y_velocity)

  def update(self):
    # if self.x < 0 or self.x > self.SCREEN_WIDTH - (self.r * 2):
    #   self.velocity = (self.velocity[0] * -1, self.velocity[1])

    if self.y < 0 or self.y > self.SCREEN_HEIGHT - (self.r * 2):
      self.velocity = (self.velocity[0], self.velocity[1] * -1)

    self.x += self.velocity[0]
    self.y += self.velocity[1]

    self.sprite.x = self.x
    self.sprite.y = self.y

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

    self.sprite = Rect(self.x, self.y, self.width, self.height, fill=0xEEEEEE, outline=0xEEEEEE)

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
    self.sprite.y = self.y

  def reset(self):
    self.y = 52
    self.sprite.y = self.y

class Score:
  def __init__(self, x, y):
    self.p1 = 0
    self.p2 = 0

    self.label = label.Label(font, text=f"{self.p1} - {self.p2}", color=0xEEEEEE)
    self.label.x = x
    self.label.y = y

  def update(self, puck):
    added = False
    if puck.x < 3:
      self.p2 += 1
      added = True
    if puck.x + puck.r > 125:
      self.p1 += 1
      added = True

    if added:
      self.label.text = f"{self.p1} - {self.p2}"
      time.sleep(1)
      puck.reset()

  def reset(self):
    self.p1 = 0
    self.p2 = 0
    self.label.text = f"{self.p1} - {self.p2}"

class Pong:
  def __init__(self, root):
    self.splash = Group()
    root.append(self.splash)
    self.splash.append(Rect(1, 1, 126, 126, fill=0x000000, outline=0x333333))
    self.left_paddle = Paddle(2, 52)
    self.splash.append(self.left_paddle.sprite)
    self.right_paddle = Paddle(122, 52)
    self.splash.append(self.right_paddle.sprite)
    self.puck = Puck(64, 64)
    self.splash.append(self.puck.sprite)
    self.score = Score(54, 8)
    self.splash.append(self.score.label)
    self.game_over = False
    self.game_over_text = label.Label(font, text="Game Over", color=0xEEEEEE)
    self.game_over_text.x = 40
    self.game_over_text.y = 64
    self.game_over_text.hidden = True
    self.splash.append(self.game_over_text)

  def update(self, btn_y, btn_x, btn_b, btn_a):
    self.left_paddle.update(not btn_y.value, not btn_b.value)
    self.right_paddle.update(not btn_x.value, not btn_a.value)
    self.puck.check_collisions(self.left_paddle, self.right_paddle)
    self.puck.update()
    self.score.update(self.puck)

    if self.score.p1 >= 3 or self.score.p2 >= 3:
      self.game_over = True
      self.game_over_text.hidden = False
      while True:
        if not btn_y.value:
          self.game_over = False
          self.game_over_text.hidden = True
          break
        if not btn_b.value:
          return
      self.score.reset()
      self.puck.reset()
      self.left_paddle.reset()
      self.right_paddle.reset()

  def has_ended(self):
    return self.game_over

  def cleanup(self, root):
    root.remove(self.splash)
