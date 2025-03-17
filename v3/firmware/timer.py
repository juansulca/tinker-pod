import random
import time
from displayio import Group, TileGrid, OnDiskBitmap
from adafruit_display_text import label
from terminalio import FONT
from adafruit_ticks import ticks_ms, ticks_diff
from digitalio import DigitalInOut
from base_app import App

COLS = 8
ROWS = 8
# list of available timers, timer value in seconds
TIMERS = [("30s", 30), ("1m", 60), ("2m", 120), ("3m", 120), ("5m", 300), ("10m", 600), ("15m", 900), ("30m", 1800)]
# Tile mapping
FILLED = 0
UP_ARROW = 1
DOWN_ARROW = 2
GO_BUTTON = 3
X_BUTTON = 4
EMPTY = 5
# colors
LABEL_COLOR = 0xEEEEEE

# preload application sprites
sprite_sheet = OnDiskBitmap("/TP_timer.bmp")

class Timer(App):
  """
  Timer application
  """
  def __init__(self, root):
    self.splash = Group()
    # load sprites into tile grid
    self.sprite = TileGrid(sprite_sheet, pixel_shader=sprite_sheet.pixel_shader, width=COLS, height=ROWS, tile_width=16, tile_height=16, default_tile=EMPTY)
    self.selected = 0
    # create label for the timer duration
    self.timer_duration = label.Label(FONT, text=TIMERS[0][0], color=LABEL_COLOR, scale=3)
    self.timer_duration.x = 42
    self.timer_duration.y = 64
    # display ui elements
    self.splash.append(self.sprite)
    self.splash.append(self.timer_duration)
    root.append(self.splash)

  def run(self, btn_y, btn_x, btn_b, btn_a, shake):
    """
    Run the timer application
    """
    last_update_time = ticks_ms()
    self.show_buttons()

    # application loop
    while True:
      now = ticks_ms()

      #run every 200ms
      if (ticks_diff(now, last_update_time) >= 200):
        if not btn_x.value:
          # increase the timer duration and update label
          self.selected = (self.selected + 1) if self.selected < len(TIMERS) - 1 else self.selected
          self.timer_duration.text = TIMERS[self.selected][0]

        if not btn_a.value:
          # decrease the timer duration and update label
          self.selected = (self.selected - 1) if self.selected > 0 else 0
          self.timer_duration.text = TIMERS[self.selected][0]

        if not btn_y.value:
          # start the countdown
          # hide duration label
          self.timer_duration.hidden = True
          # hide buttons
          self.hide_buttons()
          # create and start the countdown
          countdown = Countdown(self.sprite, TIMERS[self.selected][1])
          countdown.start(btn_b)
          # clear the tile grid
          self.clear_tile_grid()
          # wait to debounce the input
          time.sleep(0.3)
          # show the buttons and duration label
          self.show_buttons()
          self.timer_duration.hidden = False
          continue

        if not btn_b.value:
          # exit the application
          return

        last_update_time = now

  def show_buttons(self):
    """
    Show the button ui sprites on the screen
    """
    self.sprite[1, 1] = GO_BUTTON
    self.sprite[1, 6] = X_BUTTON
    self.sprite[6, 1] = UP_ARROW
    self.sprite[6, 6] = DOWN_ARROW

  def hide_buttons(self):
    """
    Hide the button ui sprites on the screen
    """
    self.sprite[1, 1] = EMPTY
    self.sprite[1, 6] = EMPTY
    self.sprite[6, 1] = EMPTY
    self.sprite[6, 6] = EMPTY

  def clear_tile_grid(self):
    """
    Clear the tile grid
    """
    # traverse the tile grid and set each tile to EMPTY
    for i in range(COLS):
      for j in range(ROWS):
        self.sprite[i, j] = EMPTY

  def cleanup(self, root):
    """
    Tear down the application
    """
    root.remove(self.splash)

class Countdown:
  """
  Countdown tracker class
  """
  def __init__(self, tile_grid: TileGrid, duration: int):
    self.sprite = tile_grid
    # set how often a tile should appear in milliseconds
    self.update_delta = (duration* 1000) // (COLS * ROWS)

  def start(self, stop_btn: DigitalInOut):
    """Initialize or restart the countdown."""
    last_update = ticks_ms()
    # create a set of empty tiles [1, 2, 3, ...]
    empty_tiles = set(range(COLS * ROWS))
    # initialize counters for the flash animation
    flash_count = 0
    flash_timer = 0
    ended = False
    # show the tile grid
    self.sprite.hidden = False

    # countdown loop
    while True:
      if not stop_btn.value:
        # stop the countdown if stop button is pressed
        return
      now = ticks_ms()

      # run every update_delta milliseconds
      if not ended and ticks_diff(now, last_update) >= self.update_delta:
        # pick random tile from the set of empty tiles
        i = random.choice(list(empty_tiles))
        # remove the selected tile
        empty_tiles.remove(i)
        # calculate the x, y position of the tile based on the index
        x = i // COLS
        y = i % ROWS
        # set the tile to filled sprite
        self.sprite[x, y] = FILLED

        last_update = now

        if len(empty_tiles) == 0:
          # end the tiles sequence and start the flash animation
          ended = True
          flash_timer = last_update

      # show the flashing animation after countdown is over
      if ended:
        # toggle the flash animation every 600ms
        if ticks_diff(now, flash_timer) >= 600:
          # initialize flash timer
          flash_timer = now
          if flash_count == 0:
            # draw arrow share on before the first flash
            self.draw_arrow()
          flash_count += 1
          self.toggle_flash()

          if flash_count > 6:
            # end the flashing animation after 5 flashes
            self.sprite.hidden = False
            # end the countdown
            return

  def toggle_flash(self):
    """
    Toggle hiding the tile grid
    """
    self.sprite.hidden = not self.sprite.hidden

  def draw_arrow(self):
    """
    Draw the arrow shape on the tile grid
    """
    self.sprite[0, 4] = EMPTY
    self.sprite[0, 5] = EMPTY
    self.sprite[0, 6] = EMPTY
    self.sprite[0, 7] = EMPTY
    self.sprite[1, 7] = EMPTY
    self.sprite[2, 7] = EMPTY
    self.sprite[3, 7] = EMPTY
    self.sprite[1, 6] = EMPTY
    self.sprite[2, 5] = EMPTY
    self.sprite[3, 4] = EMPTY
