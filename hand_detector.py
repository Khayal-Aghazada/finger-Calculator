# hand_detector.py
import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, max_hands=2, detection_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]

    def find_hands(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        return img

    def draw_hands(self, img):
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return img

    def count_fingers(self, img):
        if not self.results.multi_hand_landmarks:
            return 0

        total_fingers = 0
        handedness = self.results.multi_handedness

        for hand_index, hand_landmarks in enumerate(self.results.multi_hand_landmarks):
            hand_type = handedness[hand_index].classification[0].label  # "Left" or "Right"
            lm_list = []
            h, w, _ = img.shape
            for lm in hand_landmarks.landmark:
                lm_list.append((int(lm.x * w), int(lm.y * h)))

            fingers = []

            # Thumb: compare x-coordinate depending on hand type
            if hand_type == "Right":
                fingers.append(1 if lm_list[self.tip_ids[0]][0] < lm_list[self.tip_ids[0] - 1][0] else 0)
            else:  # Left hand
                fingers.append(1 if lm_list[self.tip_ids[0]][0] > lm_list[self.tip_ids[0] - 1][0] else 0)

            # Other fingers: tip higher than PIP
            for id in range(1, 5):
                fingers.append(1 if lm_list[self.tip_ids[id]][1] < lm_list[self.tip_ids[id] - 2][1] else 0)

            total_fingers += sum(fingers)

        return total_fingers
