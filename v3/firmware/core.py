from digitalio import DigitalInOut, Direction, Pull
from microcontroller import Pin
import board
import displayio
import adafruit_ssd1327

FPS = 60
FPS_DELAY = int(1000 / FPS)
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 128

def make_button(pin: Pin) -> DigitalInOut:
  """
  Create a digital pin set to input with the internal pull
  up resistor enabled
  pin: Pin - digital
  """
  # Create a digitla pin
  btn = DigitalInOut(pin)
  btn.direction = Direction.INPUT
  # enable internal pull up resistor
  btn.pull = Pull.UP
  return btn

def display_setup():
  displayio.release_displays()
  # use the integrated I2C STEMMA connector
  i2c = board.STEMMA_I2C()
  # match the device address, usually maked on the PCB
  display_bus = displayio.I2CDisplay(i2c, device_address=0x3D)
  # create the display controller
  display = adafruit_ssd1327.SSD1327(display_bus, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
  return display
