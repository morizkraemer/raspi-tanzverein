#!/usr/bin/env python3
"""
Main System - Clean architecture for GPIO button control with OSC
"""

import time
import threading
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

from mock_gpio import GPIO
from button_controller import ButtonController
from osc_manager import OSCManager
from osc_handler import OSCHandler

# Configuration
IP = "127.0.0.1"
IN_PORT = 9001
OUT_PORT = 7700

# Pin definitions
BUTTON_PIN = 16
LED_PINS = {
    "led1": 20,  # First LED
    "led2": 21   # Second LED
}


def start_osc_server(osc_handler):
    """Start the OSC server in a separate thread"""
    dispatcher = Dispatcher()
    dispatcher.set_default_handler(osc_handler.handle_message)

    server = osc_server.ThreadingOSCUDPServer((IP, IN_PORT), dispatcher)
    print(f"OSC server listening on {IP}:{IN_PORT}")
    print("📡 Ready to receive OSC messages...")
    server.serve_forever()


def main():
    print("🚀 Starting Tanzen Button Control System...")

    # Initialize GPIO
    GPIO.setmode(GPIO.BCM)

    # Initialize OSC client
    osc_client = SimpleUDPClient(IP, OUT_PORT)

    # Initialize system components
    osc_manager = OSCManager()
    button_controller = ButtonController(
        GPIO, BUTTON_PIN, LED_PINS, osc_client)
    osc_handler = OSCHandler(button_controller, osc_manager)

    # Start OSC server
    osc_thread = threading.Thread(
        target=start_osc_server, args=(osc_handler,), daemon=True)
    osc_thread.start()

    print("✅ System ready!")
    print("📋 Available OSC commands:")
    print("   /1/dmx/0           - Toggle button enabled/disabled")
    print("   /1/dmx/1-4         - Delay presets (5s, 15s, 30s, 60s)")
    print("   /1/path/1-5        - Button paths (/button, /trigger, /press, /action, /event)")
    print("   /1/led/1/on|off|toggle - Control LED 1")
    print("   /1/led/2/on|off|toggle - Control LED 2")
    print("   /1/led/all/on|off  - Control all LEDs")
    print("   /1/dmx/status      - Get status")
    print("-" * 50)

    try:
        while True:
            # Process button input
            button_controller.process_button()
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        button_controller.cleanup()
        GPIO.cleanup()
        print("✅ System stopped.")


if __name__ == "__main__":
    main()
