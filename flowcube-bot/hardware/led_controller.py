# hardware/led_controller.py
"""
Controls WS2812B (NeoPixel) LED strip
"""

import time
import math
try:
    from rpi_ws281x import PixelStrip, Color
except ImportError:
    print("Warning: rpi_ws281x not installed. Running in simulation mode.")
    # Mock classes for testing without hardware
    class Color:
        @staticmethod
        def __call__(r, g, b):
            return (r, g, b)
    
    class PixelStrip:
        def __init__(self, *args, **kwargs):
            self.num_pixels = kwargs.get('num', 16)
        def begin(self): pass
        def setPixelColor(self, i, color): pass
        def show(self): pass
        def numPixels(self): return self.num_pixels

from config.settings import (
    LED_PIN,
    LED_COUNT,
    LED_BRIGHTNESS,
    PULSE_SPEED,
    COLOR_OFF,
    DEBUG_MODE
)


class LEDController:
    """Controls the LED strip based on workload"""
    
    def __init__(self):
        """Initialize the LED strip"""
        self.strip = PixelStrip(
            LED_COUNT,
            LED_PIN,
            brightness=LED_BRIGHTNESS
        )
        self.strip.begin()
        self.current_color = COLOR_OFF
        self.pulse_offset = 0
        
        if DEBUG_MODE:
            print(f"[LED] Initialized {LED_COUNT} LEDs on pin {LED_PIN}")
    
    def set_color(self, color: tuple, brightness_modifier: float = 1.0):
        """
        Set all LEDs to a specific color
        
        Args:
            color: RGB tuple (r, g, b)
            brightness_modifier: Multiplier for brightness (0.0-1.0)
        """
        r, g, b = color
        
        # Apply brightness modifier
        r = int(r * brightness_modifier)
        g = int(g * brightness_modifier)
        b = int(b * brightness_modifier)
        
        self.current_color = (r, g, b)
        
        # Set all pixels to this color
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(r, g, b))
        self.strip.show()
        
        if DEBUG_MODE:
            print(f"[LED] Set color to RGB({r}, {g}, {b})")
    
    def pulse(self, color: tuple, duration: float = 2.0):
        """
        Create a pulsing effect with the given color
        
        Args:
            color: Base RGB color
            duration: How long to pulse (seconds)
        """
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Calculate pulse brightness using sine wave
            elapsed = time.time() - start_time
            brightness = (math.sin(elapsed * math.pi * 2) + 1) / 2  # 0 to 1
            brightness = 0.3 + (brightness * 0.7)  # 30% to 100%
            
            self.set_color(color, brightness)
            time.sleep(PULSE_SPEED)
    
    def animate_loading(self, color: tuple, duration: float = 1.0):
        """
        Show a loading/startup animation
        
        Args:
            color: RGB color for animation
            duration: How long the animation runs
        """
        if DEBUG_MODE:
            print("[LED] Running startup animation")
        
        # Light up LEDs one by one
        step_duration = duration / self.strip.numPixels()
        r, g, b = color
        
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(r, g, b))
            self.strip.show()
            time.sleep(step_duration)
    
    def clear(self):
        """Turn off all LEDs"""
        self.set_color(COLOR_OFF)
        if DEBUG_MODE:
            print("[LED] Cleared all LEDs")
    
    def rainbow_cycle(self, duration: float = 2.0):
        """
        Show a rainbow animation (for testing/demo)
        
        Args:
            duration: How long to run the animation
        """
        if DEBUG_MODE:
            print("[LED] Running rainbow animation")
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            for i in range(self.strip.numPixels()):
                pixel_index = (i * 256 // self.strip.numPixels())
                color = self._wheel(pixel_index & 255)
                self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(0.02)
    
    def _wheel(self, pos):
        """Generate rainbow colors across 0-255 positions"""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)