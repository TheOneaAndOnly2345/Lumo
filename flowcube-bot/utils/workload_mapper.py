# utils/workload_mapper.py
"""
Maps workload values (0-100) to colors, animations, and alerts
"""

from config.settings import (
    WORKLOAD_LOW,
    WORKLOAD_MODERATE,
    COLOR_LOW,
    COLOR_MODERATE,
    COLOR_HIGH,
    ALERT_THRESHOLD
)


class WorkloadMapper:
    """Handles mapping workload data to bot outputs"""
    
    @staticmethod
    def get_color(workload: int) -> tuple:
        """
        Get RGB color based on workload level
        
        Args:
            workload: Integer from 0-100
            
        Returns:
            RGB tuple (r, g, b)
        """
        if workload <= WORKLOAD_LOW:
            return COLOR_LOW
        elif workload <= WORKLOAD_MODERATE:
            return COLOR_MODERATE
        else:
            return COLOR_HIGH
    
    @staticmethod
    def get_status(workload: int) -> str:
        """
        Get status string based on workload level
        
        Args:
            workload: Integer from 0-100
            
        Returns:
            Status string: 'low', 'moderate', or 'high'
        """
        if workload <= WORKLOAD_LOW:
            return 'low'
        elif workload <= WORKLOAD_MODERATE:
            return 'moderate'
        else:
            return 'high'
    
    @staticmethod
    def should_alert(workload: int, previous_workload: int) -> bool:
        """
        Determine if we should trigger a voice alert
        
        Args:
            workload: Current workload (0-100)
            previous_workload: Previous workload value
            
        Returns:
            True if alert should be triggered
        """
        # Alert if crossing the threshold upward
        if workload >= ALERT_THRESHOLD and previous_workload < ALERT_THRESHOLD:
            return True
        return False
    
    @staticmethod
    def should_pulse(workload: int) -> bool:
        """
        Determine if LEDs should pulse
        
        Args:
            workload: Integer from 0-100
            
        Returns:
            True if should pulse
        """
        # Pulse effect for high workload
        return workload >= ALERT_THRESHOLD
    
    @staticmethod
    def get_brightness_modifier(workload: int) -> float:
        """
        Get brightness modifier based on workload
        Higher workload = brighter LEDs
        
        Args:
            workload: Integer from 0-100
            
        Returns:
            Float multiplier (0.3 to 1.0)
        """
        # Scale from 30% to 100% brightness
        return 0.3 + (workload / 100) * 0.7