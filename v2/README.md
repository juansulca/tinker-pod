# TinkerPod v2

TinkerPod v2 is a more advanced version of the tinkerpod. This version includes 4 buttons and an optional LiIon charger and battery.
This version can be powered using a USB-C cable with a powerbank, phone or USB-C charger.
The firmware included with this version includes more applications and a application menu.

## Parts List

| Item                              | Quantity | Description                                          |
| --------------------------------- | -------- | ---------------------------------------------------- |
| Adafruit QT PY RP2040             | 1        | Can be replaced with XIAO pinout boards              |
| Adafruit 1.5" Gray scale OLED     | 1        | SSD1327 driver chip, SPI/I2C interface               |
| TinkerPod v2 PCB                  | 1        |                                                      |
| STEMMA QT/Qwiic cable             | 1        | 50mm long                                            |
| Push buttons                      | 4        | 8mm rubber dome push buttons                         |
| Adafruit LiIon Charger BFF Add-On | 1        | (Optional battery powered)                           |
| Lithium Ion Polymer Battery       | 1        | (Optional battery powered) 3.7v – 420mAh single cell |
| Threaded Inserts                  | 8        |                                                      |
| M2 machine screws                 | 8        | M2 size bolts (4mm x2, 6mm x6)                       |
| TinkerPod v2 3D printed case      | 1        |                                                      |

## Required tools:

| Item           | Description                             |
| -------------- | --------------------------------------- |
| Soldering Iron | Preferably one with a fine tip          |
| Solder         | Rosin core, preferably thin             |
| Flux           | Paste or pen                            |
| Hex key        | Or screw driver depending on the screws |
| Twezzers       | (optional)                              |
| USB-C cable    | USB C **data** cable (USB C to C/A)     |

## Assembly

1. Flash circuit python on the QT PY RP2040.
   1. Open the official [site](https://circuitpython.org/board/adafruit_qtpy_rp2040/) and download the latest version of circuit python.
   2. While holding the _boot_ button in the QT PY, plug it into a computer using the USB-C cable. Different version of the QT PY might need a different button to access bootloader mode, please check the official [docs](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) for the specific board.
   3. The device should appears mounted in the OS as **RPI-RP2**, this might be different for other boards other than the RP2040 board.
   4. Drag and drop the `.UF2` file (downloaded in step 1) to the `RPI-RP2` boot drive.
   5. After a couple of seconds the onboard neopixel (LED) will flash and a new drive will appear in the computer, this time it should be called **CIRCUITPY**.
   6. ⚠️ Always eject the device before unplugging the cable.
   7. The device is ready to be installed.
2. (Optional) Solder the LiIon Charger BFF to the PCB.
   1. Place the PCB donut side down. The **TinkerPod** and **v2** silkscreen labels should be visible.
   2. Carefully line up the BFF with the PCB, in the M2 space, also marked as BFF LiPo charger. The JST connector (white box) should be facing the **v2** text on the PCB.
   3. Solder all the pads. take extra care on the 5V and GND pads.
3. Solder the QT PY to the PCB.
   1. Place the PCB donut side down. The **TinkerPod** and **v2** silkscreen labels should be visible.
   2. Carefully line up the QT PY with the PCB, in the `M1` space also marked on the side as `QT PY RP2040`. The pads can be identified for the cutout in the middle. Make sure the USB port is pointing towards the outside of the board and the reset and boot buttons and the STEMMA connector are accessible.
   3. Solder the **14** pins, 7 on each side.
4. Solder the 4 buttons to the PCB.
   1. After completing steps 2 and 3, flip the PCB (Donut side up).
   2. Place the buttons in the markers SW1, SW2, SW3, SW4.
   3. Flip the PCB again (Donut side down).
   4. Solder all 4 pins of every push button. (16 solder joins in total).
5. Now is a great moment to flash the firmware and test the TinkerPod before installing it into the case.
   1. Connect the STEMMA connector to the QT PY and Screen. It should slide in place without force.
   2. (Optional) Connect the battery using the JST connector in the BFF board.
   3. Download the TinkerPod firmware from GitHub. (firmware folder)
   4. Using a USB C data cable. Plug the device to the computer.
   5. Copy the content of the firmware folder (where the `code.py`file is) to the device.
   6. Do not forget to copy the `lib`directory.
   7. Alternatively install the dependencies for the firmware using `circup`.
   8. The splash screen followed by the menu should appear. Navigate the menu and use the applications by pressing the 4 buttons.
   9. The charging indicator (orange LED) in the BFF board should light up if there is a battery connected and the BFF installed.
   10. If everything works as expected, continue with the next step. If something is not working, check for cold solder joins and check that that the firmware was flashed correctly. If there is red LED flashing there is an issue with the firmware.
   11. Eject the device and unplug the USB cable.
6. Place the 3D printed buttons in the case and make sure they slide smooth.
7. Prepare the bottom case.
   1. Place the threaded inserts in the holes located in the top part of the case.
   2. Using the soldering iron push the inserts as straight as possible until they are flush with the surface of the case.
   3. Place the PCB in place (with the USB-C port towards the hole in the case) and screw it in place using the M2 machine screws.
   4. Make sure the power switch on the BFF board is in the _off_ position.
   5. Plug in the battery.
   6. Secure the battery using the battery bracket and some double sided tape.
8. Prepare the screen assembly
   1. Place the threaded inserts in the holes located in the top part of the case.
   2. Using the soldering iron push the inserts as straight as possible until they are flush with the surface of the case.
   3. Connect the STEMMA cable into the screen, it should slide in place without force.
   4. Gently place the 1.5" screen into the slot, do not apply pressure on the scree.
   5. Place the screen supports and line up the holes. The rectangular piece should go towards the top (can be placed in any orientation) and the remaining piece should go to the bottom. The bottom piece will only line up one way, with the legs pointing to the top.
   6. Screw the supports to the top case, tighten the screws until there is some resistance. Do not over tighten the screws.
   7. The screen might have some play, this is expected. And some gaps might be visible from the front side, which is also expected.
9. Closing the case.
   1. Plug the other side of the STEMMA connector to the QT PY.
   2. Using the power switch in the BFF board, turn the device _on_.
   3. Gently push the two parts of the case together.
10. Enjoy!
