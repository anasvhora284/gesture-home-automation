"""Control relays on an Arduino with hand gestures.

Webcam -> MediaPipe hand landmarks -> Keras gesture classifier -> serial command.
"""
import argparse
import os

import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model

# gesture class name -> serial command understood by the Arduino sketch
COMMANDS = {
    'okay': b'OKAY\n',               # all components ON
    'stop': b'STOP\n',               # all components OFF
    'smile': b'SMILE\n',             # relay 1 (D8) ON  - charger
    'live long': b'LIVE_LONG\n',     # relay 1 (D8) OFF
    'thumbs up': b'THUMBS_UP\n',     # relay 2 (D9) ON  - fan
    'thumbs down': b'THUMBS_DOWN\n', # relay 2 (D9) OFF
    'peace': b'PEACE\n',             # relay 3 (D10) ON - bulb
    'call me': b'CALL_ME\n',         # relay 3 (D10) OFF
    'fist': b'FIST\n',               # buzzer ON
    'rock': b'ROCK\n',               # buzzer OFF
}


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--port', default=os.environ.get('SERIAL_PORT', 'COM10'),
                   help="Arduino serial port (env SERIAL_PORT, default COM10; e.g. /dev/ttyACM0)")
    p.add_argument('--baud', type=int, default=9600)
    p.add_argument('--camera', type=int, default=0, help="webcam index")
    p.add_argument('--model-dir', default='.',
                   help="folder containing mp_hand_gesture/ and gesture.names")
    p.add_argument('--dry-run', action='store_true',
                   help="print serial commands instead of opening a port")
    return p.parse_args()


def main():
    args = parse_args()

    # Initialize mediapipe
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mpDraw = mp.solutions.drawing_utils

    # Load the gesture recognizer model and class names
    model = load_model(os.path.join(args.model_dir, 'mp_hand_gesture'))
    with open(os.path.join(args.model_dir, 'gesture.names')) as f:
        classNames = f.read().split('\n')
    print(classNames)

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise SystemExit(f"Could not open camera {args.camera}")

    arduino = None
    if not args.dry_run:
        import serial  # pyserial
        arduino = serial.Serial(args.port, args.baud)

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            x, y, c = frame.shape

            # Mirror the frame
            frame = cv2.flip(frame, 1)
            framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get hand landmark prediction
            result = hands.process(framergb)

            className = ''

            if result.multi_hand_landmarks:
                landmarks = []
                for handslms in result.multi_hand_landmarks:
                    for lm in handslms.landmark:
                        # same scaling as the original tutorial model expects
                        landmarks.append([int(lm.x * x), int(lm.y * y)])

                    mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                    # Predict gesture
                    prediction = model.predict([landmarks], verbose=0)
                    className = classNames[np.argmax(prediction)]

                    # Control Arduino based on recognized gesture
                    cmd = COMMANDS.get(className)
                    if cmd:
                        if arduino:
                            arduino.write(cmd)
                        else:
                            print(cmd)

            cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.imshow("Output", frame)

            if cv2.waitKey(1) == ord('q'):
                break
    finally:
        cap.release()
        if arduino:
            arduino.close()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
