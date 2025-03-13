# Install Dependencies for the Tinker Pod

The official documentation for installing dependencies in CircuitPython can be found [here](https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries).

## Option 1 (easy)

Copy the `lib` directory and its contents from the example or the firmware directory. to the _CIRCUITPY_ directory.

## Option 2 (harder)

Use [this](https://marketplace.visualstudio.com/items?itemName=joedevivo.vscode-circuitpython) extension from Visual Studio Code.

### How to install a dependency

1. Open the _CIRCUITPY_ directory in Visual Studio Code.
2. Use the shortcut `Ctrl+Shift+P` to open the command palette.
3. Type `CircuitPython` and select `CircuitPython: Choose CircuitPython board`.
4. Select the board, in this case `QT PY RP2040`
5. Press `Enter` to confirm the selection.
6. Use the shortcut `Ctrl+Shift+P` to open the command palette.
7. Type `CircuitPython` and select `CircuitPython: Show available libraries`.
8. Type the name of the dependency and select the option that matches the desired library.
9. Press `Enter` to confirm the selection.

## Option 3 (advanced)

Use [CircUp](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup) to install the dependencies.

1. Install and setup `circup`. Use the official guide, found [here](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/install-circup).
2. Open the terminal
3. Use the command `circup install library-name`
