
from sre_parse import IN_IGNORE
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import threading
import time

import RPi.GPIO as GPIO

IP = "127.0.0.1"
IN_PORT = 9001
OUT_PORT = 7700
OSC_BUTTON_PATH = "/button"
client = SimpleUDPClient(IP, OUT_PORT)


# Pin definitions
BUTTON_PIN = 16
LED_PIN = 20

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Active-low button
GPIO.setup(LED_PIN, GPIO.OUT)


def turn_led(on):
    GPIO.output(LED_PIN, GPIO.HIGH if on else GPIO.LOW)
    print("LED ON" if on else "LED OFF")

def handle_osc_message(address, *args):
    """Handle incoming OSC messages"""
    print(f"📨 OSC: {address} {args}")
    
    # Optional: Handle specific messages
    if address == "/led":
        if len(args) > 0:
            turn_led(bool(args[0]))

def start_osc_server():
    """Start the OSC server in a separate thread"""
    dispatcher = Dispatcher()
    
    # Map all messages to the handler (catch-all)
    dispatcher.set_default_handler(handle_osc_message)
    
    server = osc_server.ThreadingOSCUDPServer((IP, IN_PORT), dispatcher)
    print(f"OSC server listening on {IP}:{IN_PORT}")
    print("📡 Ready to receive any OSC message...")
    server.serve_forever()


def main():
    print("Starting OSC server...")
    # Start OSC server in a separate thread
    osc_thread = threading.Thread(target=start_osc_server, daemon=True)
    osc_thread.start()
    
    print("Waiting for button press...")
    turn_led(True)  # Turn on the LED initially

    button_pressed = False
    
    try:
        while True:
            current_state = GPIO.input(BUTTON_PIN)
            
            # Detect button press (transition from HIGH to LOW)
            if current_state == GPIO.LOW and not button_pressed:
                button_pressed = True
                client.send_message(OSC_BUTTON_PATH, 1)  # Button pressed
                print("Button pressed!")

                turn_led(False)
                print("Waiting 15 seconds...")
                time.sleep(15)
                turn_led(True)
                client.send_message(OSC_BUTTON_PATH, 1)  # Button released
                print("LED turned on again.")
            
            # Detect button release (transition from LOW to HIGH)
            elif current_state == GPIO.HIGH and button_pressed:
                button_pressed = False
                print("Button released, ready for next press")
            
            time.sleep(0.1)  # Check more frequently for better responsiveness
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Program stopped.")


if __name__ == "__main__":
    main()
