"""
OSC Manager System
Handles OSC message routing, path management, and delay presets
"""

class OSCManager:
    def __init__(self):
        # Button path presets
        self.button_paths = {
            1: "/button1",
            2: "/button2", 
            3: "/button3",
            4: "/button4",
            5: "/button5"
        }
        
        # Delay presets
        self.delay_presets = {
            1: 30,
            2: 60,
            3: 120,
            4: 300,  
            5: 600,
            6: 1200,
        }
        
        # Current settings
        self.current_path = 1
        self.current_delay = 30
        
    def get_button_path(self):
        """Get current button path"""
        return self.button_paths[self.current_path]
    
    def set_button_path(self, path_id):
        """Set button path by ID (1-5)"""
        if path_id in self.button_paths:
            self.current_path = path_id
            print(f"Button path set to: {self.get_button_path()}")
            return True
        else:
            print(f"Invalid path ID: {path_id}. Must be 1-5")
            return False
    
    def set_delay_preset(self, preset_id):
        """Set delay by preset ID (1-6)"""
        if preset_id in self.delay_presets:
            self.current_delay = self.delay_presets[preset_id]
            print(f"Sleep delay set to: {self.current_delay} seconds")
            return True
        else:
            print(f"Invalid delay preset: {preset_id}. Must be 1-6")
            return False
    
    def get_status(self):
        """Get current status"""
        return {
            'path': self.get_button_path(),
            'delay': self.current_delay,
            'path_id': self.current_path
        }
