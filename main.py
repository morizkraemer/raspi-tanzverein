#!/usr/bin/env python3
"""
Main System - Clean architecture for GPIO button control with OSC
"""

import time
import threading
from pythonosc.udp_client import SimpleUDPClient

from mock_gpio import GPIO
from button_controller import ButtonController
from osc_manager import OSCManager
from web_config import create_app

# Configuration
IP = "127.0.0.1"
OUT_PORT = 7700
WEB_PORT = 3001

# Pin definitions
BUTTON_PIN = 16
LED_PINS = {
    "led1": 20,  # First LED
    "led2": 21   # Second LED
}


# OSC receiving removed - button functions remain configurable

def initialize_system():
    """Initialize the button control system"""
    # Initialize GPIO
    GPIO.setmode(GPIO.BCM)
    
    # Initialize OSC client
    osc_client = SimpleUDPClient(IP, OUT_PORT)
    
    # Initialize system components
    osc_manager = OSCManager()
    button_controller = ButtonController(GPIO, BUTTON_PIN, LED_PINS, osc_client, osc_manager)
    
    return button_controller, osc_manager, osc_client

def run_button_loop(button_controller):
    """Run the button processing loop in a separate thread"""
    while True:
        button_controller.process_button()
        time.sleep(0.1)

def main():
    print("🚀 Starting Tanzen Button Control System...")
    
    # Initialize the system
    button_controller, osc_manager, osc_client = initialize_system()
    
    # Create Flask app with initialized components
    app = create_app(button_controller, osc_manager, osc_client)
    
    print("✅ System ready!")
    print("📋 Button Configuration:")
    print(f"   Current Path: {osc_manager.get_button_path()}")
    print(f"   Current Delay: {osc_manager.current_delay} seconds")
    print(f"   Button Status: {'ENABLED' if button_controller.button_enabled else 'DISABLED'}")
    print("📡 OSC Sending: Button presses send to configured path")
    print(f"🌐 Web Interface: http://localhost:{WEB_PORT}")
    print("-" * 50)
    
    # Start button processing in a separate thread
    button_thread = threading.Thread(target=run_button_loop, args=(button_controller,), daemon=True)
    button_thread.start()
    
    try:
        # Start the web interface (this will block)
        app.run(host='0.0.0.0', port=WEB_PORT, debug=False)
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        button_controller.cleanup()
        GPIO.cleanup()
        print("✅ System stopped.")


if __name__ == "__main__":
    main()
