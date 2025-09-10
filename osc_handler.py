"""
OSC Message Handler
Handles incoming OSC messages and routes them to appropriate systems
"""

class OSCHandler:
    def __init__(self, button_controller, osc_manager):
        self.button_controller = button_controller
        self.osc_manager = osc_manager
    
    def handle_message(self, address, *args):
        """Handle incoming OSC messages - only apply if argument is not 0"""
        print(f"📨 OSC: {address} {args}")
        
        # Button control (special case - 0 means disable)
        if address == "/2/dmx/0":
            if len(args) > 0:
                # Use argument value: 0 = disable, non-zero = enable
                self.button_controller.set_button_enabled(bool(args[0]))
            else:
                # No argument - toggle current state
                new_state = not self.button_controller.button_enabled
                self.button_controller.set_button_enabled(new_state)
        
        # Check if we have an argument and if it's 0 (skip if so) for other commands
        elif len(args) > 0 and args[0] == 0:
            print(f"Skipping {address} - argument is 0")
            return
        
        # Delay presets
        elif address == "/2/dmx/1":
            self.osc_manager.set_delay_preset(1)
            self.button_controller.set_sleep_delay(self.osc_manager.current_delay)
        elif address == "/2/dmx/2":
            self.osc_manager.set_delay_preset(2)
            self.button_controller.set_sleep_delay(self.osc_manager.current_delay)
        elif address == "/2/dmx/3":
            self.osc_manager.set_delay_preset(3)
            self.button_controller.set_sleep_delay(self.osc_manager.current_delay)
        elif address == "/2/dmx/4":
            self.osc_manager.set_delay_preset(4)
            self.button_controller.set_sleep_delay(self.osc_manager.current_delay)
        elif address == "/2/dmx/5":
            self.osc_manager.set_delay_preset(5)
            self.button_controller.set_sleep_delay(self.osc_manager.current_delay)
        elif address == "/2/dmx/6":
            self.osc_manager.set_delay_preset(6)
            self.button_controller.set_sleep_delay(self.osc_manager.current_delay)
        
        # Path selection
        elif address == "/2/dmx/7":
            self.osc_manager.set_button_path(1)
        elif address == "/2/dmx/8":
            self.osc_manager.set_button_path(2)
        elif address == "/2/dmx/9":
            self.osc_manager.set_button_path(3)
        elif address == "/2/dmx/10":
            self.osc_manager.set_button_path(4)
        elif address == "/2/dmx/11":
            self.osc_manager.set_button_path(5)
        
        else:
            print(f"Unknown OSC message: {address}")
