# server.py
"""
FlowCube Bot - Main Server
Receives workload data from phone app and controls hardware
"""

from flask import Flask, request, jsonify
import threading
import time
from hardware.led_controller import LEDController
from hardware.speaker_controller import SpeakerController
from utils.workload_mapper import WorkloadMapper
from config.settings import (
    SERVER_HOST,
    SERVER_PORT,
    PULSE_ENABLED,
    DEBUG_MODE
)

app = Flask(__name__)

# Initialize hardware controllers
led = LEDController()
speaker = SpeakerController()
mapper = WorkloadMapper()

# State management
current_workload = 0
previous_workload = 0
last_update_time = time.time()
is_pulsing = False


def update_hardware(workload: int):
    """
    Update all hardware based on workload value
    
    Args:
        workload: Integer from 0-100
    """
    global current_workload, previous_workload, is_pulsing
    
    previous_workload = current_workload
    current_workload = workload
    
    # Get color and status
    color = mapper.get_color(workload)
    status = mapper.get_status(workload)
    brightness = mapper.get_brightness_modifier(workload)
    
    if DEBUG_MODE:
        print(f"[Bot] Workload: {workload} | Status: {status} | Color: {color}")
    
    # Update LEDs
    if PULSE_ENABLED and mapper.should_pulse(workload):
        # Start pulsing in a separate thread to not block
        if not is_pulsing:
            is_pulsing = True
            threading.Thread(target=pulse_leds, args=(color,), daemon=True).start()
    else:
        is_pulsing = False
        led.set_color(color, brightness)
    
    # Check if we should trigger an alert
    if mapper.should_alert(workload, previous_workload):
        if workload >= 80:
            speaker.alert_overload()
        else:
            speaker.alert_high_workload()
    
    # Alert when returning to normal
    if previous_workload >= 70 and workload < 60:
        speaker.alert_back_to_normal()


def pulse_leds(color: tuple):
    """
    Continuously pulse LEDs while in high workload state
    
    Args:
        color: RGB color tuple
    """
    global is_pulsing
    
    while is_pulsing and mapper.should_pulse(current_workload):
        led.pulse(color, duration=2.0)
        time.sleep(0.1)
    
    # Reset to solid color when done pulsing
    if not is_pulsing:
        brightness = mapper.get_brightness_modifier(current_workload)
        led.set_color(color, brightness)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'current_workload': current_workload,
        'last_update': time.time() - last_update_time
    }), 200


@app.route('/workload', methods=['POST'])
def receive_workload():
    """
    Receive workload data from the phone app
    
    Expected JSON:
    {
        "globalWorkload": 62,
        "status": "moderate",
        "platformBreakdown": {
            "slack": 45,
            "jira": 62,
            "teams": 28,
            "notion": 15
        }
    }
    """
    global last_update_time
    
    try:
        data = request.get_json()
        
        if not data or 'globalWorkload' not in data:
            return jsonify({'error': 'Invalid data format'}), 400
        
        workload = data['globalWorkload']
        
        # Validate workload is in range
        if not (0 <= workload <= 100):
            return jsonify({'error': 'Workload must be between 0 and 100'}), 400
        
        # Update hardware
        update_hardware(workload)
        last_update_time = time.time()
        
        return jsonify({
            'success': True,
            'workload': workload,
            'status': mapper.get_status(workload)
        }), 200
        
    except Exception as e:
        if DEBUG_MODE:
            print(f"[Server] Error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/test', methods=['POST'])
def test_hardware():
    """
    Test endpoint to manually control hardware
    
    Expected JSON:
    {
        "action": "rainbow" | "pulse" | "clear" | "speak",
        "value": optional value (e.g., workload for pulse, message for speak)
    }
    """
    try:
        data = request.get_json()
        action = data.get('action')
        value = data.get('value')
        
        if action == 'rainbow':
            led.rainbow_cycle(duration=3.0)
        elif action == 'pulse':
            color = mapper.get_color(value or 80)
            led.pulse(color, duration=2.0)
        elif action == 'clear':
            led.clear()
        elif action == 'speak':
            message = value or "Test message"
            speaker.speak(message)
        elif action == 'beep':
            speaker.play_beep()
        else:
            return jsonify({'error': 'Unknown action'}), 400
        
        return jsonify({'success': True}), 200
        
    except Exception as e:
        if DEBUG_MODE:
            print(f"[Server] Test error: {e}")
        return jsonify({'error': str(e)}), 500


def startup_sequence():
    """Run startup animation and sound"""
    if DEBUG_MODE:
        print("[Bot] Running startup sequence...")
    
    # Animate LEDs
    led.animate_loading((0, 255, 0), duration=1.5)
    time.sleep(0.5)
    
    # Play startup sound
    speaker.play_startup_sound()
    
    # Set to idle state (low workload)
    led.set_color(mapper.get_color(0), 0.5)
    
    if DEBUG_MODE:
        print("[Bot] Startup complete! Waiting for workload data...")


if __name__ == '__main__':
    print("=" * 50)
    print("FlowCube Bot Starting...")
    print("=" * 50)
    
    # Run startup sequence
    startup_sequence()
    
    # Start the server
    print(f"\n[Server] Listening on {SERVER_HOST}:{SERVER_PORT}")
    print(f"[Server] Ready to receive workload data from app\n")
    
    app.run(
        host=SERVER_HOST,
        port=SERVER_PORT,
        debug=DEBUG_MODE,
        threaded=True
    )