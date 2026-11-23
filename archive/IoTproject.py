import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mpDraw = mp.solutions.drawing_utils

# Function to detect hand gestures


def detect_hand_gesture(hand_landmarks):
    # Extract relevant landmarks for hand gestures
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    # Extract coordinates from NormalizedLandmark objects
    thumb_tip_coords = np.array([thumb_tip.x, thumb_tip.y, thumb_tip.z])
    index_tip_coords = np.array([index_tip.x, index_tip.y, index_tip.z])
    middle_tip_coords = np.array([middle_tip.x, middle_tip.y, middle_tip.z])
    ring_tip_coords = np.array([ring_tip.x, ring_tip.y, ring_tip.z])
    pinky_tip_coords = np.array([pinky_tip.x, pinky_tip.y, pinky_tip.z])

    # Calculate distances between finger tips
    distance_thumb_index = np.linalg.norm(thumb_tip_coords - index_tip_coords)
    distance_thumb_middle = np.linalg.norm(
        thumb_tip_coords - middle_tip_coords)
    distance_thumb_ring = np.linalg.norm(thumb_tip_coords - ring_tip_coords)
    distance_thumb_pinky = np.linalg.norm(thumb_tip_coords - pinky_tip_coords)

    # Define gesture conditions
    if distance_thumb_index < 1:  # Adjust the threshold as needed
        return "Thumbs Up"
    elif distance_thumb_middle < 1:  # Adjust the threshold as needed
        return "Thumbs Down"
    elif distance_thumb_ring < 0.5:  # Adjust the threshold as needed
        return "Progressive Bar (Ring Finger)"
    elif distance_thumb_pinky < 0.5:  # Adjust the threshold as needed
        return "Progressive Bar (Pinky Finger)"
    else:
        return "No specific gesture"


# Open camera
cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image with Mediapipe Hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on the frame
            mpDraw.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Detect hand gesture
            gesture = detect_hand_gesture(hand_landmarks)

            # Print the detected gesture
            print("Detected Gesture:", gesture)

    # Display the frame
    cv2.imshow('Hand Gestures', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
