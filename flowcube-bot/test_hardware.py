#!/usr/bin/env python3
# test_hardware.py
"""
Test script to verify hardware is working correctly
Run this before starting the full server
"""

import time
import sys
from hardware.led_controller import LEDController
from hardware.speaker_controller import SpeakerController
from config.settings import COLOR_LOW, COLOR_MODERATE, COLOR_HIGH

def test_leds():
    """Test LED strip functionality"""
    print("\n" + "="*50)
    print("Testing LED Strip...")
    print("="*50)
    
    led = LEDController()
    
    print("\n1. Testing rainbow animation...")
    led.rainbow_cycle(duration=3.0)
    time.sleep(1)
    
    print("2. Testing low workload (green)...")
    led.set_color(COLOR_LOW)
    time.sleep(2)
    
    print("3. Testing moderate workload (yellow)...")
    led.set_color(COLOR_MODERATE)
    time.sleep(2)
    
    print("4. Testing high workload (red)...")
    led.set_color(COLOR_HIGH)
    time.sleep(2)
    
    print("5. Testing pulse animation...")
    led.pulse(COLOR_HIGH, duration=3.0)
    time.sleep(1)
    
    print("6. Clearing LEDs...")
    led.clear()
    
    print("\n✅ LED test complete!\n")

def test_speaker():
    """Test speaker functionality"""
    print("\n" + "="*50)
    print("Testing Speaker...")
    print("="*50)
    
    speaker = SpeakerController()
    
    print("\n1. Testing text-to-speech...")
    speaker.speak("FlowCube bot test. Can you hear me?")
    time.sleep(2)
    
    print("2. Testing alert messages...")
    speaker.alert_high_workload()
    time.sleep(3)
    
    print("3. Testing beep...")
    speaker.play_beep()
    time.sleep(1)
    
    print("\n✅ Speaker test complete!\n")

def test_combined():
    """Test LED and speaker working together"""
    print("\n" + "="*50)
    print("Testing Combined Hardware...")
    print("="*50)
    
    led = LEDController()
    speaker = SpeakerController()
    
    workload_levels = [
        (20, "Low workload"),
        (50, "Moderate workload"),
        (80, "High workload")
    ]
    
    for workload, message in workload_levels:
        print(f"\nSimulating {message} ({workload})...")
        
        # Set LED color based on workload
        if workload <= 30:
            color = COLOR_LOW
        elif workload <= 60:
            color = COLOR_MODERATE
        else:
            color = COLOR_HIGH
        
        led.set_color(color)
        speaker.speak(message)
        time.sleep(3)
    
    led.clear()
    print("\n✅ Combined test complete!\n")

def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("FlowCube Bot - Hardware Test Suite")
    print("="*50)
    print("\nThis will test all hardware components.")
    print("Make sure your LED strip and speaker are connected!")
    
    input("\nPress Enter to start testing...")
    
    try:
        # Test LEDs
        test_leds()
        time.sleep(1)
        
        # Ask if user wants to test speaker
        response = input("Test speaker? (y/n): ").lower()
        if response == 'y':
            test_speaker()
            time.sleep(1)
        
        # Test combined
        response = input("Test combined hardware? (y/n): ").lower()
        if response == 'y':
            test_combined()
        
        print("\n" + "="*50)
        print("All tests complete! 🎉")
        print("="*50)
        print("\nIf everything worked, you're ready to run server.py")
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        led = LEDController()
        led.clear()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()