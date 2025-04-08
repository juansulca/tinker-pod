# Tinkerpod v1

The TinkerPod v1 is the simplest version of the family. It is designed to be a basic introduction to the TinkerPod ecosystem.

## Part list

| Part                  | Quantity |
| --------------------- | -------- |
| Adafruit QT PY RP2040 | 1        |
| 1.5" Gray scale OLED  | 1        |
| Tiny breadboard       | 1        |
| Jumper wires          | 5        |

## 3D Printed Case

This version was tested with PLA and PETG.
The suggested orientation of the two parts is with the flat surfaces facing the build plate.
The print was made without supports with the following params:

| Param        | Value |
| ------------ | ----- |
| Layer height | 0.2mm |
| Nozzle       | 0.4mm |
| Infill       | 20%   |

The STL files can be found in the [`case/`](case/) directory.

## Firmware

The current firmware consists of the screen setup and a generative art demo.
The firmware is written in CircuitPython and works
by coping the content of the [`firmware`](firmware/) directory to the microcontroller.

### Dependencies

The firmware depends on the following libraries:

- [Adafruit CircuitPython SSD1327 driver](https://github.com/adafruit/Adafruit_CircuitPython_SSD1327)

More information about this library can be found in the official [docs](https://docs.circuitpython.org/projects/ssd1327/en/latest/)

## Assembly

1. Flash circuit python on the QT PY RP2040.

   1. Open the official [site](https://circuitpython.org/board/adafruit_qtpy_rp2040/) and download the latest version of CircuitPython.
   2. While holding the _boot_ button in the QT PY, plug it into a computer using the USB-C cable. Different version of the QT PY might need a different button to access bootloader mode, please check the official [docs](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) for the specific board.
      ![boot button location](./imgs/boot_button.jpg)
   3. The device should appears mounted in the OS as **RPI-RP2**. This might be different for other boards other than the RP2040 board.
   4. Drag and drop the `.UF2` file (downloaded in step 1) to the `RPI-RP2` drive.
   5. After a couple of seconds the onboard neopixel (LED) will flash and a new drive will appear in the computer, this time it should be called **CIRCUITPY**.
   6. ⚠️ Always eject the device before unplugging the cable.

2. Solder the headers to the QT PY.
   1. Position the headers in the QT PY and carefully place both the breadboard.
      ![header positioning](./imgs/headers_1.jpg)
   2. Solder the headers to the microcontroller.
      ![header soldering](./imgs/headers_2.jpg)
3. Place the microcontroller on the breadboard and connect the screen cable to the screen socket.
   ![screen connector placement](./imgs/screen_assembly.jpg)
4. Connect the screen to the QT PY following this diagram:
   ![Tinkerpod v1 wiring diagram](./imgs/TinkerPod_v1.png)
5. Plug the USB-C cable to the micro controller.
   ![microcontroller breadboard](./imgs/place_breadboard.jpg)
6. Check your file explorer for new drive called CIRCUITPY
7. Download the `firmware/` directory for this version.
8. Copy all the files from the `firmware/` directory (`code.py` and `lib/`) to the **CIRCUITPY** drive.
9. After the device restarts, look at the OLED screen which will display a generative art function.
10. Place the screen in the top part of the enclosure.
    ![screen in top enclosure](./imgs/screen_top_enclosure.jpg)
11. Place the breadboard in the bottom part of the enclosure.
    ![breadboard in enclosure and screen](./imgs/enclosure_components.jpg)
12. Close the enclosure with some tape.
    ![final](./imgs/final.jpg)

> ⚠️ Do not unplug the device from your computer without ejecting it properly.

## Official mods

### Add interaction with a vibration sensor

To add the same vibration sensor from version 2 to the TinkerPod v1.

Follow this schematic:

![vibration sensor schematic](./imgs/tp_v1_vibration_sensor.png)

And update the `code.py` file to use the sensor following the [button example](/examples/button).

For example:

```python
# code.py in firmware

# create the digital input for the vibration sensor on Pin A1
shake = digitalio.DigitalInOut(board.A1)
shake.direction = digitalio.Direction.INPUT
# enable pull up resistor
shake.pull = digitalio.Pull.UP

# store the shake state
was_shaken = False

while(True):
	# read the shake sensor as any other button
	if not shake.value:
		# store the shake state
		was_shaken = True

	# if the device was shaken
	if was_shaken:
		# get a random quadrant
		i = random.randint(0, 15);
		# clear the space on the screen
		clear_quadrant(i)
		# get a random draw function
		fn = random.choice(fns)
		# draw the function on the screen
		fn(i)
		# clear the shaken state
		was_shaken = False
		# wait for 0.3 seconds
		time.sleep(0.3)
```

Now the tinkerpod will react to a shake by updating the screen.
