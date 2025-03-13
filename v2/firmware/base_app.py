from digitalio import DigitalInOut
from displayio import Group

class App:
  """
  Base class for applications, each application need to block the main thread
  during its life time, when run returns the application is done and the cleanup function
  is run to clean up any resources used by the application
  """
  def run(self, btn_y: DigitalInOut, btn_x: DigitalInOut, btn_b: DigitalInOut, btn_a: DigitalInOut):
    pass

  def cleanup(self, root: Group):
    pass