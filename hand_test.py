import cv2
import mediapipe as mp
from evdev import UInput, ecodes as e

# 1. Setup Virtual Keyboard with all required keys
cap_events = {
    e.EV_KEY: [e.KEY_LEFT, e.KEY_RIGHT, e.KEY_DOWN, e.KEY_A]
}
ui = UInput(cap_events, name='python-hand-controller')

# 2. Setup MediaPipe for 1 hand
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1, 
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

url = "http://102.181.153.123:8080/video"
cap = cv2.VideoCapture(url)

# States to prevent key spamming
states = {"left": False, "right": False, "down": False, "jump": False}

def send_key(key, state_key, condition):
    if condition:
        if not states[state_key]:
            ui.write(e.EV_KEY, key, 1)
            ui.syn()
            states[state_key] = True
    else:
        if states[state_key]:
            ui.write(e.EV_KEY, key, 0)
            ui.syn()
            states[state_key] = False

while cap.isOpened():
    for _ in range(4): cap.grab()
    success, frame = cap.retrieve()
    if not success: break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Temporary logic flags for this frame
    current_left_pointing = False
    current_right_pointing = False
    current_crouching = False
    current_jumping = False

    if results.multi_hand_landmarks:
        hand_lms = results.multi_hand_landmarks[0]

        # Get key points
        index_tip = hand_lms.landmark[8]
        index_pip = hand_lms.landmark[6]

        # Finger tips and pips for open/closed detection
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]
        tips = [hand_lms.landmark[i] for i in finger_tips]
        pips = [hand_lms.landmark[i] for i in finger_pips]

        # 1. Point Right: Index tip is significantly to the right of the pip
        current_right_pointing = index_tip.x > index_pip.x + 0.05
        # 2. Point Left: Index tip is significantly to the left of the pip
        current_left_pointing = index_tip.x < index_pip.x - 0.05

        # 3. Open hand: all four finger tips above their PIP joints -> jump
        is_open = all(tip.y < pip.y for tip, pip in zip(tips, pips))
        # 4. Closed hand: all four finger tips below their PIP joints -> crouch
        is_closed = all(tip.y > pip.y for tip, pip in zip(tips, pips))

        current_jumping = is_open
        current_crouching = is_closed

        mp_draw.draw_landmarks(frame, hand_lms, mp_hands.HAND_CONNECTIONS)

    # Apply the keys based on detection
    send_key(e.KEY_LEFT, "left", current_left_pointing)
    send_key(e.KEY_RIGHT, "right", current_right_pointing)
    send_key(e.KEY_DOWN, "down", current_crouching)
    send_key(e.KEY_A, "jump", current_jumping)

    if current_jumping:
        cv2.putText(frame, "jump", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    elif current_left_pointing:
        cv2.putText(frame, "left", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    elif current_right_pointing:
        cv2.putText(frame, "right", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    elif current_crouching:
        cv2.putText(frame, "Crouch", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)


    cv2.imshow("Multi-Hand Controller", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
ui.close()
cv2.destroyAllWindows()
