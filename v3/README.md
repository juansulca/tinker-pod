# TinkerPod v3 (latest)

The latest evolution of TinkerPod delivers enhanced functionality and streamlined design through single-PCB integration. This version builds upon its predecessors, offering improved features and more robust implementation while maintaining the platform's core functionality.

The CAD and productions files for v3 con be found in the [hardware](hardware/) directory. Which is devided in:

- PCB
  - Schematic
  - PCB Layout
  - Bill of Materials
  - Gerber Files
- Case
  - Case Design
  - 3D models

The assembly instruction can be found on this page.

## v3 PCB

### Bill Of Materials

| Qty | Value                        | Package        | Designator     | Part number                              |
| :-- | ---------------------------- | -------------- | -------------- | ---------------------------------------- |
| 4   | .1uF, ceramic, 25V, 10%, X5R | 1210           | C1, C2, C3, C4 | KEMET - C1210X104K1RACTU                 |
| 2   | 10uF, ceramic, 16V, 10%, X5R | 1210           | C5, C6         | KEMET - C1210C106K3RACAUTO               |
| 1   | LED                          | 1206           | D1             | Broadcom - HSMG-C150                     |
| 1   | Schottky Diodes, 1A, 20V     | SOD-123        | D2             | onsemi - MBR120ESFT1G                    |
| 1   | B2B-PH-SM4-TB                | B2BPHSM4TBLFSN | J1             | JST - B2BPHSM4TBLFSN                     |
| 4   | 1K, 1/4W, 1%                 | 1206           | R1, R2, R3, R4 | Vishay / Beyschlag - MCA12060C1001FP500  |
| 2   | 5.1K, 1/4W, 0.1%             | 1206           | R5, R6         | Panasonic - ERA-8ARB512V                 |
| 1   | MCP73831T-2ACI/OT            | SOT-23-5       | U2             | Microchip Technology - MCP73831T-2ACI/OT |
| 1   | DPDT                         | JS202011AQN    | S5             | C&K - JS202011AQN                        |

### Assembly

1. Secure the PCB with the TP v3 label facing up.
   ![tinkerPod PCB with label facing up](./imgs/empty_pcb.jpg)
2. Apply paste in all the SMD pads, except for the QT PY pads, D1 and J1.
   1. Best results were achieved soldering the LED (D1) and JST (J1) connector with a soldering iron.
   2. Apply solder paste to the pads, but enough to cover the pad but not a blob bigger than the pad.
      ![apply solder paste](./imgs/solder_paste.jpg)
3. Use tweezers or a tiny plastic point to remove excess solder paster.
4. Place the components that do not have polarity.
   1. Place C1, C2, C3, C4 - the .1uF capacitors.
   2. Place R1, R2, R3, R4 - 1k resistors.
   3. Place C5, C6 - 10uF capacitors.
      ![place smd components](./imgs/smd_component_placement.jpg)
   4. Place R5, R6 - 5.1K resistors.
5. Place the components with polarity

   1. Place D2: diode with the line facing the closed side of the rectangle
   2. Place U2: the battery charging IC

      1. The side with 3 legs should match the side with the tiny arrow

      ![battery charging IC position](./imgs/ic_position.jpg)

6. Solder the components using a hot air reflow station.
   1. According to the specification of the solder paste, set the temperature, starts from the lowest recommended temperature.
   2. Start from far away with a medium to low airflow.
   3. Approach the individual components and make sure they fall correctly into place.
      ![hot air station soldering](./imgs/hotair_soldering.jpg)
   4. After all components are soldered, visually inspect the joints, make sure the are no pads shorting and that all the paste melted. Be careful, the PCB might be hot
      ![PCB reference](./imgs/solder_1.jpg)
   5. If there are shorting pads, retouch them with a soldering iron and some flux.
7. Solder D1 LED
   1. Check the polarity of the LED
   2. Place the LED with the Cathode (-) towards the closed side of the rectangle
   3. With the help of tweezers , solder the LED in place with a soldering iron.
      ![Solder LED](./imgs/solder_2.jpg)
8. Solder J1 JST connector.
   1. Apply some flux on the pads.
   2. Place the JST connector in place, aligning the box with the body of the connector.
   3. With the soldering iron carefully solder one of the legs of the connector.
   4. Solder the remaining legs, not much solder is needed.
      ![Solder connector](./imgs/solder_3.jpg)
9. Solder the S5 slide switch.
   1. Place the switch from the side. (TP v3 side)
      ![placing switch](./imgs/switch_place.jpg)
   2. Flip The PCB (Tinkerpod pixelated logo up)
   3. Solder the six pins.
      ![Solder solder switch](./imgs/solder_switch_pins.jpg)
10. The PCB assembly will continue in the next section.

## Parts List

| Item                          | Quantity | Description                             |
| ----------------------------- | -------- | --------------------------------------- |
| Adafruit QT PY RP2040         | 1        | Can be replaced with XIAO pinout boards |
| Adafruit 1.5" Gray scale OLED | 1        | SSD1327 driver chip, SPI/I2C interface  |
| TinkerPod v3 PCB              | 1        |                                         |
| STEMMA QT/Qwiic cable         | 1        | 50mm long                               |
| Push buttons                  | 4        | 8mm rubber dome push buttons            |
| Threaded Inserts              | 8        |                                         |
| M2 machine screws             | 8        | M2 size bolts (4mm x2, 6mm x6)          |
| TinkerPod v2 3D printed case  | 1        |                                         |

## Assembly

1. Flash circuit python on the QT PY RP2040.
   1. Open the official [site](https://circuitpython.org/board/adafruit_qtpy_rp2040/) and download the latest version of circuit python.
   2. While holding the _boot_ button in the QT PY, plug it into a computer using the USB-C cable. Different version of the QT PY might need a different button to access bootloader mode, please check the official [docs](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) for the specific board.
      ![boot button location](./imgs/boot_button.jpg)
   3. The device should appears mounted in the OS as **RPI-RP2**, this might be different for other boards other than the RP2040 board.
   4. Drag and drop the `.UF2` file (downloaded in step 1) to the `RPI-RP2` boot drive.
   5. After a couple of seconds the onboard neopixel (LED) will flash and a new drive will appear in the computer, this time it should be called **CIRCUITPY**.
   6. ⚠️ Always eject the device before unplugging the cable.
2. Solder the QT PY to the PCB.
   1. Place the PCB with the pixelated Tinkerpod logo facing down. The **TP v3** should be visible.
      ![Place qtpy on the PCB](./imgs/PCB_qtpy.jpg)
   2. Carefully line up the QT PY with the PCB, in the `QT PY RP2040` space. The pads can be identified for the cutout in the middle. Make sure the USB port is pointing towards the outside of the board and the reset and boot buttons and the STEMMA connector are accessible.
   3. Solder the **14** pins, 7 on each side.
      ![Solder QT PY pins](./imgs/solder_qtpy.jpg)
3. Solder the 4 buttons to the PCB.
   1. Flip the PCB (pixelated TinkerPod logo facing up).
   2. Place the buttons in the markers SW1, SW2, SW3, SW4.
      ![Place buttons on PCB](./imgs/place_buttons.jpg)
   3. Flip the PCB again (pixelated Tinkerpod logo facing down).
   4. Solder all 4 pins of every push button. (16 solder joins in total).
      ![Solder buttons pins](./imgs/solder_buttons.jpg)
4. Solder the vibration sensor
   1. Bend the vibration sensor legs to 90 degrees.
   2. Put the vibration sensor into the SW1 slot. The vibration sensor does not have polarity.
      ![Vibration sensor in place](./imgs/bend_sensor.jpg)
   3. If needed use some tape to secure the vibration sensor in place while soldering.
   4. Flip the PCB (Tinkerpod logo up)
   5. Solder the two pins.
      ![Solder vibration sensor pins](./imgs/solder_sensor.jpg)
   6. If the pins seem a bit long, cut them with a pair of flush cutters.
      ![Cut sensor pins](./imgs/cut_sensor_pins.jpg)
5. Now is a great moment to flash firmware and test the TinkerPod before installing it into the case.
   1. Connect the STEMMA connector to the QT PY and Screen. It should slide in place without force.
   2. (Optional) Connect the battery using the JST connector in the BFF board.
   3. Download any of the TinkerPod examples from GitHub. (examples folder)
   4. Using a USB C data cable. Plug the device to the computer.
   5. Copy the content of the firmware folder (where the `code.py`file is) to the device.
   6. Do not forget to copy the `lib`directory.
   7. Alternatively install the dependencies for the firmware using `circup`.
   8. The splash screen followed by the menu should appear. Navigate the menu and use the applications by pressing the 4 buttons.
   9. A green LED should be _on_ if there is battery connected to the JST terminal.
   10. If everything works as expected, continue with the next step. If something is not working, check for cold solder joins and check that that the firmware was flashed correctly. If there is red LED flashing there is an issue with the firmware.
   11. Eject the device and unplug the USB cable.
6. Prepare the bottom case.
   1. Slide the battery bracket on the PCB.
   2. Place the PCB in place (with the USB-C port towards the hole in the enclosure) and screw it in place using the M2 machine screws.
      ![PCB installation](./imgs/pcb_install.jpg)
   3. Push the 3D printed on/off switch and make sure the power switch is in the _off_ position (right side).
      ![Push 3D printed button in place](./imgs/push_button.jpg)
7. Prepare the screen assembly
   1. Connect the STEMMA cable into the screen, it should slide in place without force.
   2. Gently place the 1.5" screen into the slot, do not apply pressure on the screen.
   3. Place the screen supports and line up the holes. The rectangular piece should go towards the top (can be placed in any orientation) and the remaining piece should go to the bottom. The bottom piece will only line up one way, with the legs pointing to the top.
      ![Screw screen supports in place](./imgs/screw_screen.jpg)
   4. Screw the supports to the top enclosure, tighten the screws until there is some resistance. Do not over tighten the screws.
   5. The screen might have some play, this is expected. And some gaps might be visible from the front side, which is also expected.
8. Closing the enclosure.
   1. Plug the other side of the STEMMA connector to the QT PY.
      ![Plug in STEMMA connector](./imgs/assebly_no_battery.jpg)
   2. Plug in the battery.
      ![Plug in the battery](./imgs/plug_battery.jpg)
   3. Secure the battery using the battery bracket and some double-sided tape.
      ![Secure battery with double sided tape](./imgs/secure_battery.jpg)
   4. Close the enclosure
9. Turn on your device
10. Happy Tinkering!
    ![Final device](./imgs/final.jpg)
