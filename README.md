# Tanzen - GPIO Button Control System

A modular Python system for GPIO button control with OSC messaging. Features configurable delays, multiple button paths, and clean architecture.

## Hardware
- Button on GPIO pin 16 (active-low with pull-up)
- LED 1 on GPIO pin 20
- LED 2 on GPIO pin 21

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

## OSC Control System

### Button Control
- `/1/dmx/0` - Toggle button enabled/disabled

### Delay Presets
- `/1/dmx/1` - Quick (5 seconds)
- `/1/dmx/2` - Medium (15 seconds)
- `/1/dmx/3` - Long (30 seconds)
- `/1/dmx/4` - Very Long (60 seconds)

### Button Paths
- `/1/path/1` - `/button`
- `/1/path/2` - `/trigger`
- `/1/path/3` - `/press`
- `/1/path/4` - `/action`
- `/1/path/5` - `/event`

### LED Control
- `/1/led/1/on` - Turn LED 1 on
- `/1/led/1/off` - Turn LED 1 off
- `/1/led/1/toggle` - Toggle LED 1
- `/1/led/2/on` - Turn LED 2 on
- `/1/led/2/off` - Turn LED 2 off
- `/1/led/2/toggle` - Toggle LED 2
- `/1/led/all/on` - Turn all LEDs on
- `/1/led/all/off` - Turn all LEDs off

### Status
- `/1/dmx/status` - Get current status

## Architecture
- `main.py` - Main system orchestrator
- `button_controller.py` - GPIO button and LED control
- `osc_manager.py` - OSC path and delay management
- `osc_handler.py` - OSC message routing
- `mock_gpio.py` - Mock GPIO for testing
