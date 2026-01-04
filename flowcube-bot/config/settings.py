# config/settings.py
"""
FlowCube Bot Configuration
Adjust these settings based on your setup
"""

# Server Settings
SERVER_HOST = '0.0.0.0'  # Listen on all network interfaces
SERVER_PORT = 8080       # Port the app will connect to

# LED Settings
LED_PIN = 18             # GPIO pin for LED data (BCM numbering)
LED_COUNT = 12           # Number of LEDs in your strip (adjust based on your strip)
LED_BRIGHTNESS = 128     # LED brightness (0-255, 128 = 50%)

# Workload Thresholds
WORKLOAD_LOW = 30        # 0-30 = Green (low load)
WORKLOAD_MODERATE = 60   # 31-60 = Yellow (moderate load)
# 61-100 = Red (high load)

# Alert Settings
ENABLE_VOICE_ALERTS = True
ALERT_COOLDOWN = 300     # Seconds between voice alerts (5 minutes)
ALERT_THRESHOLD = 70     # Only alert if workload > 70

# LED Color Definitions (RGB values 0-255)
COLOR_LOW = (0, 255, 0)      # Green
COLOR_MODERATE = (255, 165, 0)  # Orange/Yellow
COLOR_HIGH = (255, 0, 0)     # Red
COLOR_OFF = (0, 0, 0)        # Off

# LED Animation Settings
ANIMATION_SPEED = 0.05   # Delay between animation frames (seconds)
PULSE_ENABLED = True     # Enable pulsing effect when overloaded
PULSE_SPEED = 0.03       # How fast the pulse animation runs

# Voice Alert Messages
ALERT_MESSAGES = {
    'high': "Warning: Your workload is high. Consider taking a break.",
    'overload': "Alert: You are overloaded. Time to prioritize or delegate tasks.",
    'back_to_normal': "Good news: Your workload is back to normal levels."
}

# Debug Settings
DEBUG_MODE = True        # Print debug messages
LOG_REQUESTS = True      # Log all incoming requests