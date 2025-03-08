from displayio import Group
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
import terminalio
from pong import Pong
from tiling import Tiling

font = terminalio.FONT

class Button:
  def __init__(self, x, y, text):
    self.x = x
    self.y = y
    self.d = 32
    self.sprite = Group()
    self.label = label.Label(font, text=text, color=0x888888, x=self.x + 9, y=self.y + 16, scale=3)
    self.sprite.append(Rect(x, y, self.d, self.d, fill=0x000000, outline=0x888888))
    self.sprite.append(self.label)

  def pressed(self, btn):
    if btn:
      self.label.color = 0xDDDDDD
    else:
      self.label.color = 0x888888


class Menu:
  def __init__(self, root):
    self.playing = False
    self.splash = Group()
    root.append(self.splash)

    self.app = None
    self.y = Button(0, 0, "Y")
    self.splash.append(self.y.sprite)

    self.x = Button(96, 0, "X")
    self.splash.append(self.x.sprite)

    self.b = Button(0, 96, "B")
    self.splash.append(self.b.sprite)

    self.a = Button(96, 96, "A")
    self.splash.append(self.a.sprite)
  
  def hide_buttons(self):
    self.y.sprite.hidden = True
    self.x.sprite.hidden = True
    self.b.sprite.hidden = True
    self.a.sprite.hidden = True
  
  def show_buttons(self):
    self.y.sprite.hidden = False
    self.x.sprite.hidden = False
    self.b.sprite.hidden = False
    self.a.sprite.hidden = False

  def update(self, btn_y, btn_x, btn_b, btn_a):
    if not self.playing:
      self.y.pressed(not btn_y.value)
      self.x.pressed(not btn_x.value)
      self.b.pressed(not btn_b.value)
      self.a.pressed(not btn_a.value)

      if not btn_y.value:
        self.hide_buttons()
        self.app = Pong(self.splash)
        self.playing = True
      
      if not btn_x.value:
        print("x pressed")
        self.hide_buttons()
        self.app = Tiling(self.splash)
        self.playing = True
    else:
      if self.app:
        self.app.update(btn_y, btn_x, btn_b, btn_a)
        if self.app.has_ended():
          self.app.cleanup(self.splash)
          self.app = None
          self.playing = False
          self.show_buttons()