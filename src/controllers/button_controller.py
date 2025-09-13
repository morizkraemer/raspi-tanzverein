"""
Button Controller System
Handles GPIO button input, LED control, and OSC messaging
"""

import time
import threading
from pythonosc.udp_client import SimpleUDPClient
from .led_controller import LEDController

class ButtonController:
    def __init__(self, gpio, button_pin, osc_client, osc_manager, led_controller):
        self.gpio = gpio
        self.button_pin = button_pin
        self.osc_client = osc_client
        self.osc_manager = osc_manager
        
        # State
        self.button_pressed = False
        self.button_enabled = True
        self.is_button_blocked = False
        
        # Setup GPIO
        self.gpio.setup(self.button_pin, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)

        # Setup LEDs using LEDController
        self.led_controller = led_controller
        
    
    def set_button_enabled(self, enabled):
        """Enable or disable button functionality"""
        self.button_enabled = enabled
        print(f"Button functionality {'ENABLED' if enabled else 'DISABLED'}")
        
        # Set red LED state based on button enabled status
        if enabled:
            self.led_controller.switch_red_led(False)  # Red LED off when enabled
            self.led_controller.switch_green_led(True)  # Green LED on when enabled
        else:
            self.led_controller.switch_red_led(True)   # Red LED on when disabled
            self.led_controller.switch_green_led(False) # Green LED off when disabled
    
    def process_button(self):
        """Process button input - call this in main loop"""
        current_state = self.gpio.input(self.button_pin)
        
        # Detect button press (transition from HIGH to LOW)
        if current_state == self.gpio.LOW and not self.button_pressed:
            self.button_pressed = True
            self._handle_button_press()
    
        # Detect button release (transition from LOW to HIGH)
        elif current_state == self.gpio.HIGH and self.button_pressed:
            self.button_pressed = False
            print("Button released, ready for next press")
    
    def _handle_button_press(self):
        """Handle button press sequence"""
        print("Button pressed!")

        if not self.button_enabled or self.is_button_blocked:
            self.led_controller.blink_red_led(blink_rate=0.2, times=3)
            print("Button functionality disabled or blocked - showing red blink feedback")
            return
        
        # Get current OSC path from manager
        osc_path = self.osc_manager.get_button_path()
        
        # Send OSC message to current path
        self.osc_client.send_message(osc_path, 1)
        print(f"Sent OSC: {osc_path} = 1")
        
        # Start effect duration timer in a separate thread
        effect_thread = threading.Thread(target=self._run_effect_duration, args=(osc_path,), daemon=True)
        effect_thread.start()
        
        # Start block timer in a separate thread
        block_delay = self.osc_manager.current_delay
        if block_delay > 0:
            self.is_button_blocked = True
            print(f"Blocking button for {block_delay} seconds...")
            block_thread = threading.Thread(target=self._run_block_timer, args=(block_delay,), daemon=True)
            block_thread.start()
        else:
            print("No block delay - immediate release")
    
    def _run_block_timer(self, block_delay):
        """Run block timer in separate thread"""
        # During block: green off, red on (blocked state)
        self.led_controller.switch_green_led(False)
        self.led_controller.switch_red_led(True)
        time.sleep(block_delay)
        self.is_button_blocked = False
        
        # After block: restore to enabled state (green on, red off)
        if self.button_enabled:
            self.led_controller.switch_green_led(True)
            self.led_controller.switch_red_led(False)
        print("Button unblocked - LEDs restored to enabled state.")
    
    def _run_effect_duration(self, osc_path):
        """Run effect duration timer in separate thread"""
        osc_off_delay = self.osc_manager.current_osc_off_delay
        self.led_controller.blink_green_led(duration=self.osc_manager.current_osc_off_delay, blink_rate=0.4)
        if osc_off_delay > 0:
            print(f"Effect duration: {osc_off_delay} seconds...")
            time.sleep(osc_off_delay)

        else:
            print("No effect duration - ending immediately")
            
        self.osc_client.send_message(osc_path, 1)
        print(f"Sent OSC: {osc_path} = 0")
    
    def cleanup(self):
        """Clean up resources"""
        self.led_controller.switch_all_leds(False)
        print("Button controller cleaned up")
