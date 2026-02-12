# main.py
import cv2
from camera import Camera
from gesture_engine import GestureEngine
from input_controller import InputController
from config import CAMERA_URL, KEY_BINDINGS, MP_CONFIG


def draw_debug(frame, lines):
    y = 30
    for line in lines:
        cv2.putText(
            frame,
            line,
            (10, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )
        y += 20


def main():
    camera = Camera(CAMERA_URL)
    gesture_engine = GestureEngine(MP_CONFIG)
    input_controller = InputController(KEY_BINDINGS)

    while True:
        frame = camera.read()
        if frame is None:
            break

        frame, actions, debug_lines = gesture_engine.process(frame)
        input_controller.update(actions)

        draw_debug(frame, debug_lines)

        cv2.imshow("Hand Controller (Modular)", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    input_controller.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
