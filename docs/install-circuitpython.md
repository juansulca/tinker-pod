# How to Install CircuitPython on Adafruit QT PY RP2040

To flash CircuitPython onto your Adafruit QT PY RP2040, follow these steps:

1. Open the official [site](https://circuitpython.org/board/adafruit_qtpy_rp2040/) and download the latest version of circuit python.
2. While holding the _boot_ button in you QT PY, plug it into your computer using the USB-C cable.
   Different version of the QT PY (the non-RP2040 variants) might need a different button to access bootloader mode,
   please check the official [docs](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) for the board you are using.
3. The device should appears mounted in your OS as **RPI-RP2**, this might be different if you are not using an RP2040 board.
4. Drag and drop the `.UF2` file you downloaded in step 1 to the `RPI-RP2` boot drive.
5. After a couple of seconds some lights will flash and a new drive will appear in your computer, this time it should be called **CIRCUITPY**.
6. ⚠️ Always eject your device before removing it.
7. Your device is ready to be installed.

The official docs to install CircuitPython can be found [here](https://learn.adafruit.com/adafruit-qt-py-2040/circuitpython)
