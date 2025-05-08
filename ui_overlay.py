# ui_overlay.py
import cv2

def draw_text(img, text, position=(50, 50), color=(0, 255, 0), scale=1, thickness=2):
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness)
    return img
