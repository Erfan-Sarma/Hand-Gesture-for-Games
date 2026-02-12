import cv2
import mediapipe as mp

# ---------------------
# MediaPipe setup
# ---------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# ---------------------
# Camera
# ---------------------
url = "http://192.168.1.12:8080/video"
cap = cv2.VideoCapture(url)

# ---------------------
# Predefined colors for 21 joints (BGR)
# Each index has a unique, readable color
# ---------------------
JOINT_COLORS = [
    (255, 255, 255),  # 0  Wrist - white

    (255, 0, 0),      # 1  Thumb CMC - blue
    (255, 64, 64),    # 2  Thumb MCP
    (255, 128, 128),  # 3  Thumb IP
    (255, 180, 180),  # 4  Thumb TIP

    (0, 255, 0),      # 5  Index MCP - green
    (64, 255, 64),    # 6  Index PIP
    (128, 255, 128),  # 7  Index DIP
    (180, 255, 180),  # 8  Index TIP

    (0, 0, 255),      # 9  Middle MCP - red
    (64, 64, 255),    # 10 Middle PIP
    (128, 128, 255),  # 11 Middle DIP
    (180, 180, 255),  # 12 Middle TIP

    (0, 255, 255),    # 13 Ring MCP - yellow
    (64, 255, 255),   # 14 Ring PIP
    (128, 255, 255),  # 15 Ring DIP
    (180, 255, 255),  # 16 Ring TIP

    (255, 0, 255),    # 17 Pinky MCP - purple
    (255, 64, 255),   # 18 Pinky PIP
    (255, 128, 255),  # 19 Pinky DIP
    (255, 180, 255),  # 20 Pinky TIP
]

# ---------------------
# Main loop
# ---------------------
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Mirror frame so visualization matches user
    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:

            # Draw hand skeleton lightly
            mp_draw.draw_landmarks(
                frame,
                hand_lms,
                mp_hands.HAND_CONNECTIONS,
                mp_draw.DrawingSpec(color=(150, 150, 150), thickness=1),
                mp_draw.DrawingSpec(color=(150, 150, 150), thickness=1),
            )

            # Draw each joint with its own color + index
            for idx, lm in enumerate(hand_lms.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                color = JOINT_COLORS[idx]

                # draw joint
                cv2.circle(frame, (cx, cy), 6, color, -1)

                # label index
                cv2.putText(
                    frame,
                    str(idx),
                    (cx + 5, cy - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    1
                )

    cv2.imshow("Hand Joint Index & Color Debugger", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()