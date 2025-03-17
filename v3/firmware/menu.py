from displayio import Group, TileGrid, OnDiskBitmap
from pong import Pong
from tiling import Tiling
from timer import Timer
from draw import Draw
from adafruit_ticks import ticks_ms, ticks_diff
from base_app import App

# preload the menu sprites from disk
sprite_sheet = OnDiskBitmap("/TP_menu.bmp")
menu_sprite_sheet = OnDiskBitmap("/TP_menu_icons.bmp")

# list of available applications
apps = [Pong, Tiling, Timer, Draw]
apps_len = len(apps)

BUTTON_SPIRTE_MAP =[
  (4, 1), # y
  (2, 5), # x
  (0, 1), # b
  (2, 3), # a
]

def load_button_sprite(sprite_map: tuple[int, int]) -> TileGrid:
  sprite = TileGrid(sprite_sheet, pixel_shader=sprite_sheet.pixel_shader, width=2, height=1, tile_width=16, tile_height=16)
  sprite[0] = sprite_map[0]
  sprite[1] = sprite_map[1]
  return sprite

class Button:
  """
  Class to represent a button on the screen
  """
  def __init__(self, x: int, y: int, sprite: TileGrid):
    # buttons are 16x16 two part sprites
    self.group = Group(scale=2)
    self.sprite = sprite
    self.group.append(sprite)
    self.group.x = x
    self.group.y = y
    self.pressed_i = (sprite[0], sprite[1])

  # def pressed(self, btn):
  #    """
  #    Handdle button pressed sprite change
  #    """
  #   if btn:
  #     self.sprite[0] = self.pressed_i[0] + 6
  #     self.sprite[1] = self.pressed_i[1] + 6
  #   else:
  #     self.sprite[0] = self.pressed_i[0]
  #     self.sprite[1] = self.pressed_i[1]

class Menu(App):
  """
  Class to represent the main menu, display different applications
  and orquestate the execution
  """
  def __init__(self, root):
    # create group for the view
    self.splash = Group()
    # load icon sprite, scale and position it on screen
    self.icon_sprite = TileGrid(menu_sprite_sheet, pixel_shader=menu_sprite_sheet.pixel_shader, width=1, height=1, tile_width=32, tile_height=32)
    self.app_icon = Group(scale=2)
    self.app_icon.append(self.icon_sprite)
    self.app_icon.x = 32
    self.app_icon.y = 32
    root.append(self.splash)
    root.append(self.app_icon)
    # set the initial application index
    self.i = 0
    self.app = None

    # create UI buttons
    sprite_y = load_button_sprite(BUTTON_SPIRTE_MAP[0])
    self.y = Button(0, 0, sprite_y)
    self.splash.append(self.y.group)

    sprite_x = load_button_sprite(BUTTON_SPIRTE_MAP[1])
    self.x = Button(64, 0, sprite_x)
    self.splash.append(self.x.group)

    sprite_b = load_button_sprite(BUTTON_SPIRTE_MAP[2])
    self.b = Button(0, 96, sprite_b)
    self.splash.append(self.b.group)

    sprite_a = load_button_sprite(BUTTON_SPIRTE_MAP[3])
    self.a = Button(64, 96, sprite_a)
    self.splash.append(self.a.group)

  def hide_ui(self):
    """
    Hide UI elements
    """
    self.y.group.hidden = True
    self.x.group.hidden = True
    self.b.group.hidden = True
    self.a.group.hidden = True
    self.app_icon.hidden = True

  def show_ui(self):
    """
    Show UI elements
    """
    self.y.group.hidden = False
    self.x.group.hidden = False
    self.b.group.hidden = False
    self.a.group.hidden = False
    self.app_icon.hidden = False

  def run(self, btn_y, btn_x, btn_b, btn_a, shake):
    """
    Execute the Menu application
    """
    last_input_time = ticks_ms()
    while True:
      # self.y.pressed(not btn_y.value)
      # self.x.pressed(not btn_x.value)
      # self.b.pressed(not btn_b.value)
      # self.a.pressed(not btn_a.value)

      # get current time
      now = ticks_ms()

      if ticks_diff(now, last_input_time) > 200:
        if not btn_y.value:
          # previous application
          self.i = (self.i - 1) if self.i > 0 else apps_len - 1
          self.icon_sprite[0] = self.i

        if not btn_x.value:
          # next application
          self.i = (self.i + 1) % apps_len
          self.icon_sprite[0] = self.i

        if not btn_a.value:
          # run application
          # Hide UI elements
          self.hide_ui()
          # create new application instance
          self.app = apps[self.i](self.splash)
          # run the application
          self.app.run(btn_y, btn_x, btn_b, btn_a, shake)
          # after application is done run teardown
          self.app.cleanup(self.splash)
          # destroy application instance
          self.app = None
          # show the UI elements
          self.show_ui()

        if not (btn_b.value and btn_a.value and btn_x.value and btn_y.value):
          # if any of the buttons was pressed update the last input time
          last_input_time = now
