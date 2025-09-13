#!/usr/bin/env python3
"""
Test script for button functionality without web server
"""

import time
import threading
from pythonosc.udp_client import SimpleUDPClient

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gpio.gpio_handler import GPIO, setup_gpio
from src.controllers.button_controller import ButtonController
from src.managers.osc_manager import OSCManager
from src.controllers.led_controller import LEDController

# Configuration
IP = "127.0.0.1"
OUT_PORT = 7700
BUTTON_PIN = 16
LED_PINS = {
    "led_green": 21,
    "led_red": 21
}

def run_button_loop(button_controller):
    """Run the button processing loop"""
    while True:
        button_controller.process_button()
        time.sleep(0.1)

def main():
    print("🧪 Starting Button Test (No Web Server)...")
    
    # Initialize GPIO (automatically uses real or mock GPIO)
    GPIO.setmode(GPIO.BCM)
    setup_gpio()
    
    # Initialize OSC client
    osc_client = SimpleUDPClient(IP, OUT_PORT)
    
    # Initialize system components
    osc_manager = OSCManager()
    led_controller = LEDController(GPIO, LED_PINS)
    button_controller = ButtonController(GPIO, BUTTON_PIN, osc_client, osc_manager, led_controller)
    
    print("✅ System ready!")
    print("📋 Button Configuration:")
    print(f"   Current Scene: {osc_manager.get_button_path()}")
    print(f"   Block Delay: {osc_manager.current_delay} seconds")
    print(f"   Effect Duration: {osc_manager.current_osc_off_delay} seconds")
    print(f"   Button Status: {'ENABLED' if button_controller.button_enabled else 'DISABLED'}")
    print("📡 OSC Sending: Button presses send to configured path")
    print("-" * 50)
    print("🎮 Press ENTER to simulate button press (Ctrl+C to exit)")
    
    # Start button processing in a separate thread
    button_thread = threading.Thread(target=run_button_loop, args=(button_controller,), daemon=True)
    button_thread.start()
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        button_controller.cleanup()
        GPIO.cleanup()
        print("✅ Test stopped.")

if __name__ == "__main__":
    main()
