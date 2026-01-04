# hardware/speaker_controller.py
"""
Controls speaker for voice alerts using text-to-speech
"""

import time
import subprocess
from config.settings import (
    ENABLE_VOICE_ALERTS,
    ALERT_COOLDOWN,
    ALERT_MESSAGES,
    DEBUG_MODE
)


class SpeakerController:
    """Handles audio alerts and text-to-speech"""
    
    def __init__(self):
        """Initialize the speaker controller"""
        self.last_alert_time = 0
        self.last_alert_type = None
        
        if DEBUG_MODE:
            print("[Speaker] Initialized")
    
    def speak(self, message: str):
        """
        Use text-to-speech to speak a message
        
        Args:
            message: Text to speak
        """
        if not ENABLE_VOICE_ALERTS:
            if DEBUG_MODE:
                print(f"[Speaker] Voice alerts disabled. Would say: {message}")
            return
        
        if DEBUG_MODE:
            print(f"[Speaker] Speaking: {message}")
        
        try:
            # Use espeak for text-to-speech (pre-installed on Raspberry Pi OS)
            subprocess.run(
                ['espeak', message],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            # Fallback to festival if espeak not available
            try:
                subprocess.run(
                    ['echo', message, '|', 'festival', '--tts'],
                    shell=True,
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except:
                if DEBUG_MODE:
                    print("[Speaker] Text-to-speech not available")
    
    def alert_high_workload(self):
        """Play alert for high workload"""
        if not self._can_alert('high'):
            return
        
        message = ALERT_MESSAGES.get('high', "Your workload is high.")
        self.speak(message)
        self._update_alert_time('high')
    
    def alert_overload(self):
        """Play alert for overload condition"""
        if not self._can_alert('overload'):
            return
        
        message = ALERT_MESSAGES.get('overload', "You are overloaded.")
        self.speak(message)
        self._update_alert_time('overload')
    
    def alert_back_to_normal(self):
        """Play alert when workload returns to normal"""
        # No cooldown for positive alerts
        message = ALERT_MESSAGES.get('back_to_normal', "Workload is normal.")
        self.speak(message)
        self.last_alert_type = 'normal'
    
    def play_startup_sound(self):
        """Play a sound when the bot starts"""
        self.speak("FlowCube bot is online and monitoring your workload.")
    
    def play_beep(self, frequency: int = 1000, duration: float = 0.2):
        """
        Play a simple beep sound
        
        Args:
            frequency: Beep frequency in Hz
            duration: Beep duration in seconds
        """
        if DEBUG_MODE:
            print(f"[Speaker] Beep: {frequency}Hz for {duration}s")
        
        try:
            # Use speaker-test to generate a tone
            subprocess.run(
                ['speaker-test', '-t', 'sine', '-f', str(frequency), '-l', '1'],
                timeout=duration,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except:
            if DEBUG_MODE:
                print("[Speaker] Could not play beep")
    
    def _can_alert(self, alert_type: str) -> bool:
        """
        Check if enough time has passed since last alert
        
        Args:
            alert_type: Type of alert
            
        Returns:
            True if alert can be played
        """
        current_time = time.time()
        time_since_last = current_time - self.last_alert_time
        
        # Don't repeat the same alert type within cooldown period
        if self.last_alert_type == alert_type and time_since_last < ALERT_COOLDOWN:
            if DEBUG_MODE:
                remaining = ALERT_COOLDOWN - time_since_last
                print(f"[Speaker] Alert cooldown active. {remaining:.0f}s remaining")
            return False
        
        return True
    
    def _update_alert_time(self, alert_type: str):
        """Update the last alert timestamp"""
        self.last_alert_time = time.time()
        self.last_alert_type = alert_type