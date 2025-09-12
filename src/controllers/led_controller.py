import time
import threading

class LEDController:
    def __init__(self, gpio, pins):
        self.gpio = gpio
        self.pins = pins
        self.leds = {}
        for pin in self.pins:
            self.leds[pin] = LED(gpio, pin)

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

    def cleanup(self):
        """Clean up LED resources"""
        for led_name in self.leds:
            self.leds[led_name].cleanup()
    
    def blink_green_led(self, duration=1.0, blink_rate=0.5, times=None):
        """Blink green LED"""
        print(f"🟢 Green LED: Starting blink for {duration}s (rate: {blink_rate}s, times: {times})")
        self.leds["led_green"].blink(duration, blink_rate, times)
    
    def blink_red_led(self, duration=1.0, blink_rate=0.5, times=None):
        """Blink red LED"""
        print(f"🔴 Red LED: Starting blink for {duration}s (rate: {blink_rate}s, times: {times})")
        self.leds["led_red"].blink(duration, blink_rate, times)
    
    def blink_all_leds(self, duration=1.0, blink_rate=0.5, times=None):
        """Blink all LEDs"""
        print(f"💡 All LEDs: Starting blink for {duration}s (rate: {blink_rate}s, times: {times})")
        for led_name in self.leds:
            self.leds[led_name].blink(duration, blink_rate, times)
    
    def switch_green_led(self, state):
        """Switch green LED on or off"""
        print(f"🟢 Green LED: {'ON' if state else 'OFF'}")
        self.leds["led_green"].switch(state)
        
    def switch_red_led(self, state):
        """Switch red LED on or off"""
        print(f"🔴 Red LED: {'ON' if state else 'OFF'}")
        self.leds["led_red"].switch(state)
        
    def switch_all_leds(self, state):
        """Switch all LEDs on or off"""
        print(f"💡 All LEDs: {'ON' if state else 'OFF'}")
        for led_name in self.leds:
            self.leds[led_name].switch(state)


class LED:
    def __init__(self, gpio, pin):
        """
        Initialize LED with GPIO instance and pin number

        Args:
            gpio: GPIO instance (RPi.GPIO or mock_gpio)
            pin: GPIO pin number for the LED
        """
        self.gpio = gpio
        self.pin = pin
        self.is_on = False
        self.is_blinking = False
        self._blink_thread = None
        self._blink_stop_event = threading.Event()

        # Setup the pin as output
        self.gpio.setup(self.pin, self.gpio.OUT)
        self.turn_off()  # Start with LED off

    def switch(self, on):
        """Switch the LED on or off"""
        self.turn_on() if on else self.turn_off()

    def turn_on(self):
        """Turn the LED on"""
        self.gpio.output(self.pin, self.gpio.HIGH)
        self.is_on = True
        print(f"LED on pin {self.pin}: ON")

    def turn_off(self):
        """Turn the LED off"""
        self.gpio.output(self.pin, self.gpio.LOW)
        self.is_on = False
        print(f"LED on pin {self.pin}: OFF")

    def toggle(self):
        """Toggle LED state"""
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()

    def blink(self, duration=1.0, blink_rate=0.5, times=None):
        """
        Make the LED blink

        Args:
            duration: Total duration to blink (seconds)
            blink_rate: Time between blinks (seconds)
            times: Number of blinks (if None, blinks for duration)
        """
        if self.is_blinking:
            print(f"LED on pin {self.pin}: Stopping previous blink")
            self.stop_blink()

        self.is_blinking = True
        self._blink_stop_event.clear()
        print(f"LED on pin {self.pin}: Starting blink (duration: {duration}s, rate: {blink_rate}s, times: {times})")

        self._blink_thread = threading.Thread(
            target=self._blink_worker,
            args=(duration, blink_rate, times),
            daemon=True
        )
        self._blink_thread.start()

    def _blink_worker(self, duration, blink_rate, times):
        """Worker function for blinking in a separate thread"""
        start_time = time.time()
        blink_count = 0

        try:
            while not self._blink_stop_event.is_set():
                # Check if we've reached the duration limit
                if duration and (time.time() - start_time) >= duration:
                    break

                # Check if we've reached the blink count limit
                if times and blink_count >= times:
                    break

                # Toggle LED
                self.toggle()
                blink_count += 1

                # Wait for blink rate
                if self._blink_stop_event.wait(blink_rate):
                    break

        finally:
            self.is_blinking = False
            # Ensure LED is off when blinking stops
            self.turn_off()
            print(f"LED on pin {self.pin}: Blink completed")

    def stop_blink(self):
        """Stop the LED from blinking"""
        if self.is_blinking:
            self._blink_stop_event.set()
            if self._blink_thread and self._blink_thread.is_alive():
                self._blink_thread.join(timeout=1.0)
            self.is_blinking = False
            print(f"LED on pin {self.pin}: Blinking stopped")

    def cleanup(self):
        """Clean up LED resources"""
        self.stop_blink()
        self.turn_off()
        print(f"LED on pin {self.pin}: Cleaned up")
