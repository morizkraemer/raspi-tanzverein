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
- `/2/dmx/0` - Enable/disable button (0=disable, 1=enable, no arg=toggle)

### Delay Presets
- `/2/dmx/1` - 30 seconds
- `/2/dmx/2` - 60 seconds
- `/2/dmx/3` - 120 seconds
- `/2/dmx/4` - 300 seconds
- `/2/dmx/5` - 600 seconds
- `/2/dmx/6` - 1200 seconds

### Button Paths
- `/2/dmx/7` - `/button`
- `/2/dmx/8` - `/trigger`
- `/2/dmx/9` - `/press`
- `/2/dmx/10` - `/action`
- `/2/dmx/11` - `/event`

### Button Behavior
When button is pressed, it sends OSC messages to the currently selected path:
- Press: `{selected_path} = 1`
- Release: `{selected_path} = 0`

## Architecture
- `main.py` - Main system orchestrator
- `button_controller.py` - GPIO button and LED control
- `osc_manager.py` - OSC path and delay management
- `osc_handler.py` - OSC message routing
- `mock_gpio.py` - Mock GPIO for testing
