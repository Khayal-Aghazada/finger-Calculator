# main.py
import cv2
import time
from hand_detector import HandDetector
from gesture_logic import interpret_operation, is_equal_gesture
from ui_overlay import draw_text

# New helper class to manage state-specific confirmation
class StateTimer:
    def __init__(self):
        self.last_value = None
        self.start_time = 0

    def is_confirmed(self, current_value, hold_time=2):
        now = time.time()
        if current_value != self.last_value:
            self.last_value = current_value
            self.start_time = now
            return False
        return (now - self.start_time) >= hold_time

# Setup
cap = cv2.VideoCapture(0)
detector = HandDetector()

# State management
state = 'WAIT_FIRST'
first_number = None
second_number = None
operation = None
result = None

# Separate timers for each state
timers = {
    'WAIT_FIRST': StateTimer(),
    'WAIT_OP': StateTimer(),
    'WAIT_SECOND': StateTimer(),
    'WAIT_EQUAL': StateTimer(),
    'SHOW_RESULT': StateTimer()
}

while True:
    success, img = cap.read()
    if not success:
        break

    img = detector.find_hands(img)
    finger_count = detector.count_fingers(img)

    if state == 'WAIT_FIRST':
        draw_text(img, "Show FIRST number (1–10) for 2s", (50, 50))
        if 1 <= finger_count <= 10 and timers[state].is_confirmed(finger_count):
            first_number = finger_count
            state = 'WAIT_OP'

    elif state == 'WAIT_OP':
        draw_text(img, "Operation: 1.+ 2.- 3.* 4./ (Hold 2s)", (50, 50))
        op = interpret_operation(finger_count)
        if op and timers[state].is_confirmed(finger_count):
            operation = op
            state = 'WAIT_SECOND'

    elif state == 'WAIT_SECOND':
        draw_text(img, "Show SECOND number (1 to 10) for 2s", (50, 50))
        if 1 <= finger_count <= 10 and timers[state].is_confirmed(finger_count):
            second_number = finger_count
            state = 'WAIT_EQUAL'

    elif state == 'WAIT_EQUAL':
        draw_text(img, "Show '=' (thumbs up) for 2s", (50, 50))
        if is_equal_gesture(finger_count, detector) and timers[state].is_confirmed(finger_count):
            try:
                result = eval(f"{first_number} {operation} {second_number}")
            except ZeroDivisionError:
                result = "Error (Divide by 0)"
            state = 'SHOW_RESULT'

    elif state == 'SHOW_RESULT':
        draw_text(img, f"{first_number} {operation} {second_number} = {result}", (50, 50), color=(0, 0, 255))
        draw_text(img, "Show FIST (0 fingers) for 2s to restart", (50, 100))
        if finger_count == 0 and timers[state].is_confirmed(finger_count):
            first_number = second_number = operation = result = None
            state = 'WAIT_FIRST'
            for t in timers.values():
                t.last_value = None  # Reset timers fully

    img = detector.draw_hands(img)
    cv2.imshow("Finger Math", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()