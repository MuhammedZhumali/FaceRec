import RPi.GPIO as GPIO
import time
import subprocess
from collections import deque

# === GPIO pin configuration (UPDATED) ===
TRIG = 23 
ECHO = 24 

# === Detection settings ===
MIN_DISTANCE = 20       # in cm
MAX_DISTANCE = 50      # in cm
REQUIRED_DETECTIONS = 3 # number of consecutive valid measurements
SAMPLES_WINDOW = 5      # size of smoothing buffer
MEASURE_DELAY = 0.4     # time between measurements in seconds

# === GPIO setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# === Distance buffer and trigger counter ===
distance_history = deque(maxlen=SAMPLES_WINDOW)
trigger_counter = 0

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = None
    pulse_end = None

    timeout = time.time() + 1
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if time.time() > timeout:
            break

    timeout = time.time() + 1
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if time.time() > timeout:
            break

    if pulse_start is None or pulse_end is None:
        return None

    pulse_duration = pulse_end - pulse_start
    return round(pulse_duration * 17150, 2)

def get_filtered_distance():
    d = get_distance()
    if d is None or d < 2 or d > 100:
        return None
    distance_history.append(d)
    return sum(distance_history) / len(distance_history)

try:
    print(f"📡 Waiting for someone to approach ({MIN_DISTANCE}–{MAX_DISTANCE} cm)...")
    while True:
        distance = get_filtered_distance()
        if distance:
            print(f"📏 Distance: {distance:.1f} cm")
            if MIN_DISTANCE <= distance <= MAX_DISTANCE:
                trigger_counter += 1
                print(f"✅ Confirmation {trigger_counter}/{REQUIRED_DETECTIONS}")
            else:
                trigger_counter = 0
        else:
            print("⚠️ No valid response from sensor")

        if trigger_counter >= REQUIRED_DETECTIONS:
            print("🚀 Person detected! Launching face recognition...")
            subprocess.run(["python3", "face_recognition"])
            trigger_counter = 0

        time.sleep(MEASURE_DELAY)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("🛑 Stopped by user")