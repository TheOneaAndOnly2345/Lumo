# hardware/display_controller.py
"""
Optional LCD Display Controller
For future enhancement: Show workload number on small screen
"""

from config.settings import DEBUG_MODE


class DisplayController:
    """Controls optional LCD display (e.g., 16x2 or OLED)"""
    
    def __init__(self):
        """Initialize display (if connected)"""
        self.enabled = False  # Set to True if display is connected
        
        if DEBUG_MODE:
            print("[Display] Display controller initialized (no display connected)")
    
    def show_workload(self, workload: int, status: str):
        """
        Display workload value and status on screen
        
        Args:
            workload: Integer from 0-100
            status: Status string ('low', 'moderate', 'high')
        """
        if not self.enabled:
            return
        
        # TODO: Add LCD display code here when hardware is added
        # Example for 16x2 LCD:
        # self.lcd.clear()
        # self.lcd.message(f"Workload: {workload}\nStatus: {status}")
        
        if DEBUG_MODE:
            print(f"[Display] Would show: Workload {workload} - {status}")
    
    def show_message(self, message: str):
        """
        Display a custom message
        
        Args:
            message: Text to display
        """
        if not self.enabled:
            return
        
        # TODO: Add LCD display code here
        
        if DEBUG_MODE:
            print(f"[Display] Would show: {message}")
    
    def clear(self):
        """Clear the display"""
        if not self.enabled:
            return
        
        # TODO: Add LCD display code here
        
        if DEBUG_MODE:
            print("[Display] Cleared")
    
    def set_backlight(self, on: bool):
        """
        Turn display backlight on/off
        
        Args:
            on: True to turn on, False to turn off
        """
        if not self.enabled:
            return
        
        # TODO: Add LCD backlight control here
        
        if DEBUG_MODE:
            print(f"[Display] Backlight: {'ON' if on else 'OFF'}")