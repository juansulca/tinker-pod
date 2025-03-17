from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
import terminalio
import time
from displayio import Group
from core import FPS_DELAY, SCREEN_HEIGHT
from base_app import App
from adafruit_ticks import ticks_ms, ticks_diff
from random import choice

font = terminalio.FONT

class Paddle:
  """
  Represents a paddle in the pong game
  """
  def __init__(self, x: int, y: int):
    self.x = x
    self.y = y
    self.width = 4
    self.height = 24
    self.velocity = 0
    # draw paddle as a rectangle
    self.sprite = Rect(self.x, self.y, self.width, self.height, fill=0xEEEEEE, outline=0xEEEEEE)

  def update(self, up: bool, down: bool):
    """
    Update the paddle position and velocity based on the button state
    """
    if up and self.y > 0:
      # move up if the button is pressed and the paddle is not at the top
      self.velocity = -1
    else:
      self.velocity = 0

    if down and self.y < SCREEN_HEIGHT - 1 - self.height:
      # move down if the button is pressed and the paddle is not at the bottom
      self.velocity = 1

    if not up and not down:
      # stop the paddle if no button is pressed
      self.velocity = 0

    # move paddle based on the velocity
    self.y += self.velocity
    # update the sprite y position
    self.sprite.y = self.y

  def reset(self):
    """Reset the paddle position"""
    self.y = 52
    self.sprite.y = self.y

class Puck:
  """
  Represents the puck in the pong game
  """
  def __init__(self, x: int, y: int):
    self.x = x
    self.y = y
    # store the velocity of the puck (vx, vy)
    self.velocity = (1, 0)
    # radius of the puck
    self.r = 4
    # puck sprite
    self.sprite = Rect(self.x, self.y, self.r, self.r, fill=0xDDDDDD, outline=0xDDDDDD)
  def check_collisions(self, paddle_l: Paddle, paddle_r: Paddle):
    """
    Check if the puck collides with the paddles
    """
    if self.x <= paddle_l.x + paddle_l.width/2 and paddle_l.y <= self.y <= paddle_l.y + paddle_l.height:
      # bounce the puck with the left paddle
      y_velocity = self.velocity[1] if paddle_l.velocity == 0 else paddle_l.velocity
      self.velocity = (-self.velocity[0], y_velocity)

    if self.x >= paddle_r.x - paddle_r.width/2 and paddle_r.y <= self.y <= paddle_r.y + paddle_r.height:
      # bounce the puck with the right paddle
      y_velocity = self.velocity[1] if paddle_r.velocity == 0 else paddle_r.velocity
      self.velocity = (-self.velocity[0], y_velocity)

  def update(self):
    """
    update the puck position and velocity
    """
    if self.y < 0 or self.y > SCREEN_HEIGHT - (self.r * 2):
      # bounce the puck with the top and bottom walls
      self.velocity = (self.velocity[0], self.velocity[1] * -1)

    # calculate new position based on the speed
    self.x += self.velocity[0]
    self.y += self.velocity[1]

    # update sprite position
    self.sprite.x = self.x
    self.sprite.y = self.y

  def reset(self):
    """
    Reset the puck position and velocity
    """
    self.x = 64
    self.y = 64
    # velocity is random but always to the left or right
    self.velocity = (choice([1, -1]), 0)


class Score:
  """Represents the score board the game"""
  def __init__(self, x: int, y: int):
    # player scores
    self.p1 = 0
    self.p2 = 0
    # create label
    self.label = label.Label(font, text=f"{self.p1} - {self.p2}", color=0xEEEEEE)
    self.label.x = x
    self.label.y = y

  def update(self, puck: Puck):
    """Update the score based on the puck position"""
    added = False
    if puck.x < 3:
      # add a point to player 2 if the puck reached the left zone
      self.p2 += 1
      added = True
    if puck.x + puck.r > 125:
      # add a point to player 1 if the puck reached the right zone
      self.p1 += 1
      added = True

    if added:
      # update the label text and reset the puck if points were added
      self.label.text = f"{self.p1} - {self.p2}"
      # wait before restarting the game
      time.sleep(1)
      puck.reset()

  def reset(self):
    """Reset the score"""
    self.p1 = 0
    self.p2 = 0
    self.label.text = f"{self.p1} - {self.p2}"

class Pong(App):
  """Pong game application"""
  def __init__(self, root):
    self.splash = Group()
    root.append(self.splash)
    # draw the game board
    self.splash.append(Rect(1, 1, 126, 126, fill=0x000000, outline=0x333333))
    # create and display paddles
    self.left_paddle = Paddle(2, 52)
    self.splash.append(self.left_paddle.sprite)
    self.right_paddle = Paddle(122, 52)
    self.splash.append(self.right_paddle.sprite)
    # create and display the puck
    self.puck = Puck(64, 64)
    self.splash.append(self.puck.sprite)
    # create and display the score board
    self.score = Score(54, 8)
    self.splash.append(self.score.label)
    self.game_over = False # game over state
    # create game over text
    self.game_over_text = label.Label(font, text="Game Over", color=0xEEEEEE)
    self.game_over_text.x = 40
    self.game_over_text.y = 64
    # hide the game over text
    self.game_over_text.hidden = True
    # add the game over text to the view
    self.splash.append(self.game_over_text)

  def run(self, btn_y, btn_x, btn_b, btn_a, shake=None):
    last_update_time = ticks_ms()
    while True:
      now = ticks_ms()

      # game runs at 60 FPS
      if ticks_diff(now, last_update_time) >= FPS_DELAY:
        # update paddle positions
        self.left_paddle.update(not btn_y.value, not btn_b.value)
        self.right_paddle.update(not btn_x.value, not btn_a.value)
        # bounce the puck with the paddles
        self.puck.check_collisions(self.left_paddle, self.right_paddle)
        self.puck.update()
        # update score board
        self.score.update(self.puck)

        if self.score.p1 >= 3 or self.score.p2 >= 3:
          # show game over text if any player reaches 3 points
          self.game_over_text.hidden = False
          while (True):
            # wait for user input
            if not btn_y.value:
              # restart the game
              self.game_over_text.hidden = True
              last_update_time = ticks_ms()
              self.score.reset()
              self.puck.reset()
              self.left_paddle.reset()
              self.right_paddle.reset()
              break
            if not btn_b.value:
              # exit the game
              return

        last_update_time = now

  def cleanup(self, root):
    """Tear down the pong game application"""
    root.remove(self.splash)
