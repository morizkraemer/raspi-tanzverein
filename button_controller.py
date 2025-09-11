"""
Button Controller System
Handles GPIO button input, LED control, and OSC messaging
"""

import time
import threading
from pythonosc.udp_client import SimpleUDPClient

class ButtonController:
    def __init__(self, gpio, button_pin, led_pins, osc_client, osc_manager):
        self.gpio = gpio
        self.button_pin = button_pin
        self.led_pins = led_pins  # Dictionary of LED names to pins
        self.osc_client = osc_client
        self.osc_manager = osc_manager
        
        # State
        self.button_pressed = False
        self.button_enabled = True
        
        # Setup GPIO
        self.gpio.setup(self.button_pin, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)
        
        # Setup LEDs
        for led_name, led_pin in self.led_pins.items():
            self.gpio.setup(led_pin, self.gpio.OUT)
            print(f"LED '{led_name}' on pin {led_pin}")
        
        # Start with all LEDs off
        self.turn_all_leds(False)
    
    def turn_led(self, led_name, on):
        """Turn specific LED on or off"""
        if led_name in self.led_pins:
            led_pin = self.led_pins[led_name]
            self.gpio.output(led_pin, self.gpio.HIGH if on else self.gpio.LOW)
            print(f"LED '{led_name}' {'ON' if on else 'OFF'}")
        else:
            print(f"Unknown LED: {led_name}")
    
    def turn_all_leds(self, on):
        """Turn all LEDs on or off"""
        for led_name in self.led_pins:
            self.turn_led(led_name, on)
    
    def toggle_led(self, led_name):
        """Toggle specific LED state"""
        if led_name in self.led_pins:
            led_pin = self.led_pins[led_name]
            current_state = self.gpio.input(led_pin)
            new_state = not bool(current_state)
            self.turn_led(led_name, new_state)
        else:
            print(f"Unknown LED: {led_name}")
    
    def set_button_enabled(self, enabled):
        """Enable or disable button functionality"""
        self.button_enabled = enabled
        print(f"Button functionality {'ENABLED' if enabled else 'DISABLED'}")
    
    def process_button(self):
        """Process button input - call this in main loop"""
        if not self.button_enabled:
            # Reset button state if disabled
            if self.button_pressed:
                self.button_pressed = False
                print("Button functionality disabled - resetting state")
            return
        
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
        
        # Get current OSC path from manager
        osc_path = self.osc_manager.get_button_path()
        
        # Send OSC message to current path
        self.osc_client.send_message(osc_path, 1)
        print(f"Sent OSC: {osc_path} = 1")
        
        # Turn off all LEDs
        self.turn_all_leds(False)
        
        # Start effect duration timer in a separate thread
        effect_thread = threading.Thread(target=self._run_effect_duration, args=(osc_path,), daemon=True)
        effect_thread.start()
        
        # Handle block delay in main thread
        block_delay = self.osc_manager.current_delay
        if block_delay > 0:
            print(f"Blocking button for {block_delay} seconds...")
            time.sleep(block_delay)
        else:
            print("No block delay - immediate release")
        
        # Turn all LEDs back on when block is released
        self.turn_all_leds(True)
        print("All LEDs turned on again - button unblocked.")
    
    def _run_effect_duration(self, osc_path):
        """Run effect duration timer in separate thread"""
        osc_off_delay = self.osc_manager.current_osc_off_delay
        
        if osc_off_delay > 0:
            print(f"Effect duration: {osc_off_delay} seconds...")
            time.sleep(osc_off_delay)
        else:
            print("No effect duration - ending immediately")
            
        self.osc_client.send_message(osc_path, 0)
        print(f"Sent OSC: {osc_path} = 0")
    
    def cleanup(self):
        """Clean up resources"""
        self.turn_all_leds(False)
        print("Button controller cleaned up")
