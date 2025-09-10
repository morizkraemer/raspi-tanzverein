from pythonosc.udp_client import SimpleUDPClient
import time

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    from mock_gpio import GPIO  # Use mock GPIO if not on Raspberry Pi
    using_mock = True
else:
    using_mock = False

IP = "127.0.0.1"
PORT = 7700
OSC_BUTTON_PATH = "/button"
client = SimpleUDPClient(IP, PORT)


# Pin definitions
BUTTON_PIN = 21
LED_PIN = 20

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Active-low button
GPIO.setup(LED_PIN, GPIO.OUT)


def turn_led(on):
    GPIO.output(LED_PIN, GPIO.HIGH if on else GPIO.LOW)
    print("LED ON" if on else "LED OFF")


def main():
    print("Waiting for button press...")
    turn_led(True)  # Turn on the LED initially

    # Start keyboard monitoring if using mock GPIO
    if using_mock:
        GPIO.start_keyboard_monitoring()

    try:
        while True:
            if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                client.send_message(OSC_BUTTON_PATH, 1)  # Button pressed
                print("Button pressed!")
                turn_led(False)
                print("Waiting 15 seconds...")
                time.sleep(15)
                turn_led(True)
                client.send_message(OSC_BUTTON_PATH, 1)  # Button released
                print("LED turned on again.")
            time.sleep(0.5)  # Check less frequently to reduce output spam
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Program stopped.")


if __name__ == "__main__":
    main()
