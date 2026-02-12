# gesture_engine.py
import cv2
import mediapipe as mp


class GestureEngine:
    def __init__(self, mp_config):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(**mp_config)
        self.drawer = mp.solutions.drawing_utils

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        actions = {
            "left": False,
            "right": False,
            "down": False,
            "jump": False
        }

        debug_lines = []

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_lms, handedness in zip(
                results.multi_hand_landmarks,
                results.multi_handedness
            ):
                label = handedness.classification[0].label.lower()
                lm = hand_lms.landmark

                self.drawer.draw_landmarks(
                    frame, hand_lms, self.mp_hands.HAND_CONNECTIONS
                )

                if label == "left":
                    jump = lm[8].x > lm[6].x
                    crouch = lm[20].x > lm[18].x

                    actions["jump"] |= jump
                    actions["down"] |= crouch

                    debug_lines.append("LEFT HAND:")
                    debug_lines.append(f" Jump: {jump}")
                    debug_lines.append(f" Crouch: {crouch}")

                elif label == "right":
                    go_right = lm[4].x > lm[1].x
                    go_left = (lm[8].x < lm[6].x) and not go_right

                    actions["right"] |= go_right
                    actions["left"] |= go_left

                    debug_lines.append("RIGHT HAND:")
                    debug_lines.append(f" Go Right: {go_right}")
                    debug_lines.append(f" Go Left: {go_left}")

        # Priority logic
        if actions["jump"]:
            actions["left"] = actions["right"] = actions["down"] = False
        elif actions["down"]:
            actions["left"] = actions["right"] = False

        return frame, actions, debug_lines
