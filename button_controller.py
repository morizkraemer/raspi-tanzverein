"""
Button Controller System
Handles GPIO button input, LED control, and OSC messaging
"""

import time
import threading
from pythonosc.udp_client import SimpleUDPClient

class ButtonController:
    def __init__(self, gpio, button_pin, led_pins, osc_client):
        self.gpio = gpio
        self.button_pin = button_pin
        self.led_pins = led_pins  # Dictionary of LED names to pins
        self.osc_client = osc_client
        
        # State
        self.button_pressed = False
        self.button_enabled = True
        self.sleep_delay = 15  # Default 15 seconds
        
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
    
    def set_sleep_delay(self, delay):
        """Set the sleep delay in seconds"""
        self.sleep_delay = delay
        print(f"Sleep delay set to: {delay} seconds")
    
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
        
        # Send OSC message
        self.osc_client.send_message("/button", 1)
        
        # Turn off all LEDs and wait
        self.turn_all_leds(False)
        print(f"Waiting {self.sleep_delay} seconds...")
        time.sleep(self.sleep_delay)
        
        # Turn all LEDs back on and send release message
        self.turn_all_leds(True)
        self.osc_client.send_message("/button", 0)
        print("All LEDs turned on again.")
    
    def cleanup(self):
        """Clean up resources"""
        self.turn_all_leds(False)
        print("Button controller cleaned up")
