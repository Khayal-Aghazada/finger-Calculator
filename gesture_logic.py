# gesture_logic.py

def interpret_operation(finger_count):
    return {
        1: '+',
        2: '-',
        3: '*',
        4: '/',
    }.get(finger_count, None)

def is_equal_gesture(finger_count, hand_detector):
    # Thumb up (1 finger) and likely in vertical position
    return finger_count == 1
