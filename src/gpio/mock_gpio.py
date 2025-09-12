import time
import threading
import sys
import select
import tty
import termios

class GPIO:
    BCM = 'BCM'
    OUT = 'OUT'
    IN = 'IN'
    HIGH = 1
    LOW = 0
    PUD_UP = 'PUD_UP'

    _pin_state = {}
    _pin_mode = {}
    _keyboard_thread = None
    _keyboard_running = False
    _button_pin = None

    @staticmethod
    def setmode(mode):
        print(f"[MOCK GPIO] Mode set to {mode}")

    @staticmethod
    def setup(pin, mode, pull_up_down=None):
        GPIO._pin_mode[pin] = mode
        if mode == GPIO.IN:
            GPIO._pin_state[pin] = GPIO.HIGH if pull_up_down == GPIO.PUD_UP else GPIO.LOW
            # Store the button pin for keyboard monitoring
            GPIO._button_pin = pin
        else:
            GPIO._pin_state[pin] = GPIO.LOW
        print(f"[MOCK GPIO] Pin {pin} set as {mode}, pull {pull_up_down}")

    @staticmethod
    def input(pin):
        state = GPIO._pin_state.get(pin, GPIO.LOW)
        # Only print when state changes to reduce spam
        if not hasattr(GPIO, '_last_state') or GPIO._last_state != state:
            print(f"[MOCK GPIO] Read pin {pin}: {state}")
            GPIO._last_state = state
        return state

    @staticmethod
    def output(pin, state):
        GPIO._pin_state[pin] = state
        print(f"[MOCK GPIO] Set pin {pin} to {'HIGH' if state else 'LOW'}")

    @staticmethod
    def cleanup():
        print(f"[MOCK GPIO] Cleaning up")
        GPIO._stop_keyboard_monitoring()
        GPIO._pin_state.clear()
        GPIO._pin_mode.clear()

    @staticmethod
    def start_keyboard_monitoring():
        """Start monitoring keyboard input for button simulation"""
        if GPIO._keyboard_thread is None or not GPIO._keyboard_thread.is_alive():
            GPIO._keyboard_running = True
            GPIO._keyboard_thread = threading.Thread(target=GPIO._keyboard_monitor, daemon=True)
            GPIO._keyboard_thread.start()
            print("[MOCK GPIO] Keyboard monitoring started. Press ENTER or SPACE to simulate button press.")

    @staticmethod
    def _stop_keyboard_monitoring():
        """Stop keyboard monitoring"""
        GPIO._keyboard_running = False
        if GPIO._keyboard_thread and GPIO._keyboard_thread.is_alive():
            GPIO._keyboard_thread.join(timeout=0.1)

    @staticmethod
    def _keyboard_monitor():
        """Monitor keyboard input in a separate thread"""
        import os
        
        while GPIO._keyboard_running:
            try:
                # Use a simpler approach that doesn't interfere with output
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    char = sys.stdin.read(1)
                    if char in ['\n', '\r', ' ']:  # Enter or Space key
                        if GPIO._button_pin is not None:
                            print(f"\n[MOCK GPIO] Keyboard input detected - simulating button press!")
                            GPIO._pin_state[GPIO._button_pin] = GPIO.LOW
                            time.sleep(0.6)  # Hold for 0.6 seconds to ensure detection
                            GPIO._pin_state[GPIO._button_pin] = GPIO.HIGH
                    elif char == 'q':  # Quit
                        print(f"\n[MOCK GPIO] Quit key pressed")
                        GPIO._keyboard_running = False
                        break
            except:
                # If there's any issue with input, just continue
                time.sleep(0.1)

    # Simulate changing the state for testing
    @staticmethod
    def simulate_button_press(pin, duration=0.5):
        """Simulate a button being pressed (active LOW)"""
        GPIO._pin_state[pin] = GPIO.LOW
        print(f"[MOCK GPIO] Simulate button press on pin {pin}")
        time.sleep(duration)
        GPIO._pin_state[pin] = GPIO.HIGH
        print(f"[MOCK GPIO] Simulate button release on pin {pin}")
