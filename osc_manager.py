"""
OSC Manager System
Handles OSC message routing, path management, and delay presets
"""

class OSCManager:
    def __init__(self):
        # QLC Scene presets
        self.button_paths = {
            1: "Scene A",
            2: "Scene B", 
            3: "Scene C",
            4: "Scene D",
            5: "Scene E"
        }
        
        # Delay presets
        self.delay_presets = {
            0: 0,     # No delay
            1: 30,    # 30 seconds
            2: 60,    # 1 minute
            3: 300,   # 5 minutes
            4: 1800,  # 30 minutes
            5: 3600,  # 1 hour
            6: 7200,  # 2 hours
        }
        
        # Current settings
        self.current_path = 1
        self.current_delay = 30  # Block delay (how long button is blocked)
        self.current_osc_off_delay = 30  # OSC off delay (when to send release message)
        
    def get_button_path(self):
        """Get current QLC scene"""
        return self.button_paths[self.current_path]
    
    def set_button_path(self, path_id):
        """Set QLC scene by ID (1-5)"""
        if path_id in self.button_paths:
            self.current_path = path_id
            print(f"QLC scene set to: {self.get_button_path()}")
            return True
        else:
            print(f"Invalid scene ID: {path_id}. Must be 1-5")
            return False
    
    def set_delay_preset(self, preset_id):
        """Set delay by preset ID (0-6)"""
        if preset_id in self.delay_presets:
            self.current_delay = self.delay_presets[preset_id]
            if self.current_delay == 0:
                print("Sleep delay set to: NO DELAY (immediate)")
            else:
                print(f"Sleep delay set to: {self.current_delay} seconds")
            return True
        else:
            print(f"Invalid delay preset: {preset_id}. Must be 0-6")
            return False
    
    def get_status(self):
        """Get current status"""
        return {
            'scene': self.get_button_path(),
            'delay': self.current_delay,
            'osc_off_delay': self.current_osc_off_delay,
            'scene_id': self.current_path
        }
