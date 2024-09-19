# TinkerPod

Open-Source | DIY | Multitool | Modular | Extendable

The TinkerPod a is digital multitool, a DIY device designed to engage with creative and curious minds.
Drawing inspiration from gadgets like the Flipper Zero and Pwnagotchi, this project is built following
the principles of Critical Engineering and Open-Source Hardware. The TinkerPod is an ideal multitool
for designers and makers to explore, learn, modify and extend; make it your own!

## Version 0.99 (latest)
The TinkerPod is currently in development, and the first version is expected to be released soon.

## Part list
| Part                  | Quantity |
| --------------------- | -------- |
| Adafruit QT PY RP2040 | 1        |
| 1.5" Gray scale OLED  | 1        |
| Tiny breadboard       | 1        |
| Jumper wires          | 5        |

## 3D Printed Case
3D print the case. This version was tested using Prusa mini with PLA. But the model should work with other materials and printers.
The suggested orientation of the two parts is with the flat surfaces facing the build plate.
This might be different for a resin 3D printers.
The print was made without supports with the following params:

| Param        | Value |
| ------------ | ----- |
| Layer height | 0.2mm |
| Nozzle       | 0.4mm |
| Infill       | 20%   |

The STL files can be found in the `case/` directory.

## Firmware
The current firmware consists of the screen setup and two generative art demos. The firmware is written in CircuitPython and should work
by coping the content of the `firmware` directory to your microcontroller.

### Dependencies
The firmware depends on the following libraries:
- `adafruit_ssd1327.mpy`

More information about this library can be found in the official [docs](https://docs.circuitpython.org/projects/ssd1327/en/latest/)

## Assembly
1. Ensure your microcontroller has its pins soldered.
2. Place your microcontroller in the the breadboard.
3. Connect your screen cable to the screen socket.
4. Wire the screen cables following this diagram:
```
  QT PY             Screen
┌───┐          ┌───┐
│ A2  ┼──────┼ CS  │
│     │          │     │
│ A3  ┼──────┼ DC  │
│     │          │     │
│ GND ┼──────┼ GND │
│     │          │     │
│ 3V  ┼──────┼ VCC │
│     │          │     │
│ M0  ┼──────┼ DIN │
│     │          │     │
│ SCK ┼──────┼ CLK │
└───┘          └───┘
```

5. Plug your USB C cable to your micro controller. If its the first time your using this microcontroller you might need to press the `boot` button located here:
6. A new device should show up in your file system. Usually the device will be called `CIRCUITPY`
7. Download the `code.py` file from this repository.
8. Copy and paste the file to the device in your file system.
9. By this time, you should be able to see something in your screen.
10. Install dependencies. There should be two options:
	1. Install circuit python and use its library manager.
	2. Copy and paste the files from this repo `firmware/lib` to the `lib` folder in the root directory of your microcontroller.
11. Your device should be up and running now.
12. Place the screen in the top part of the case as follows:
13. Place the breadboard in the bottom part of the case.
14. Close the case with some tape.

> ⚠️ Do not unplug the device from your computer without ejecting it properly.
This can cause the firmware to go away.
