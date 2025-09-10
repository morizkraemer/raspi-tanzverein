# Simple python script to read raspi gpio pins and trigger osc 

A Python script that reads a button on GPIO pin 21 and sends OSC messages when pressed. Includes mock GPIO for testing on non-Raspberry Pi systems.

## Hardware
- Button on GPIO pin 21 (active-low with pull-up)
- LED on GPIO pin 20

## Usage
```bash
python main.py
```

## Testing
On non-Raspberry Pi systems, press Enter or Space to simulate button press.

## Dependencies
```bash
pip install -r requirements.txt
pip install RPi.GPIO  # Only on Raspberry Pi
```

## OSC Messages
- Sends `/button` message to `127.0.0.1:7700` when button is pressed
