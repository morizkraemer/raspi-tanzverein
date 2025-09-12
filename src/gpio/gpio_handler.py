"""
GPIO Handler - Automatically uses RPi.GPIO when available, falls back to mock GPIO
"""

try:
    import RPi.GPIO as GPIO
    print("[GPIO] Using real RPi.GPIO")
    USING_MOCK_GPIO = False
except ImportError:
    from .mock_gpio import GPIO
    print("[GPIO] RPi.GPIO not available, using mock GPIO")
    USING_MOCK_GPIO = True

def setup_gpio():
    """Setup GPIO and start keyboard monitoring if using mock"""
    if USING_MOCK_GPIO:
        GPIO.start_keyboard_monitoring()
        print("[GPIO] Keyboard monitoring enabled (Enter/Space to simulate button)")
    else:
        print("[GPIO] Using real hardware GPIO")
