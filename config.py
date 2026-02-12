# config.py
from evdev import ecodes as e

CAMERA_URL = "http://192.168.1.12:8080/video"

KEY_BINDINGS = {
    "left":  e.KEY_LEFT,
    "right": e.KEY_RIGHT,
    "down":  e.KEY_DOWN,
    "jump":  e.KEY_A
}

MP_CONFIG = {
    "max_num_hands": 2,
    "min_detection_confidence": 0.7,
    "min_tracking_confidence": 0.7
}
