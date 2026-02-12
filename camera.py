# camera.py
import cv2

class Camera:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)

    def read(self):
        success, frame = self.cap.read()
        if not success:
            return None

        frame = cv2.flip(frame, 1)
        return frame

    def release(self):
        self.cap.release()
