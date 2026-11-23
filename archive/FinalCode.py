import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model
import serial  # Import the pyserial library
import speech_recognition as sr
import tkinter as tk
from PIL import Image, ImageTk

# Initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognizer model
model = load_model('mp_hand_gesture')

# Load class names
f = open('gesture.names', 'r')
classNames = [name.lower() for name in f.read().split('\n') if name]
f.close()
print(classNames)

# Initialize serial communication with Arduino
# Replace 'COM3' with the appropriate port for your Arduino
arduino = serial.Serial('COM9', 9600)

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Function to toggle speech recognition


def toggle_speech_recognition():
    global speech_recognition_on
    speech_recognition_on = not speech_recognition_on
    if speech_recognition_on:
        speech_button.config(text="Turn Off Speech Recognition")
        listen_for_speech()
    else:
        speech_button.config(text="Turn On Speech Recognition")

# Function to listen for speech


def listen_for_speech():
    if speech_recognition_on:
        with sr.Microphone() as source:
            print("Say something:")
            try:
                audio = recognizer.listen(
                    source, timeout=None)  # Listen indefinitely
                text = recognizer.recognize_google(audio)
                print("You said:", text)
                # Control Arduino based on recognized speech
                if "bulb on" in text:
                    arduino.write(b'6')
                    listen_for_speech()
                elif "bulb off" in text:
                    arduino.write(b'5')
                    listen_for_speech()
                elif "fan on" in text:
                    arduino.write(b'8')
                    listen_for_speech()
                elif "fan off" in text:
                    arduino.write(b'2')
                    listen_for_speech()
                elif "fist" in text:
                    arduino.write(b'10')
                    listen_for_speech()
                elif "rock" in text:
                    arduino.write(b'7')
                    listen_for_speech()
                elif "socket on" in text:
                    arduino.write(b'4')
                    listen_for_speech()
                elif "socket off" in text:
                    arduino.write(b'3')
                    listen_for_speech()
                elif "exit" in text:
                    exit()  # Exit the program
                elif "camera" in text:
                    toggle_camera()  # Toggle camera mode
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(
                    "Could not request results from Google Speech Recognition service; {0}".format(e))


# Function to toggle camera
def toggle_camera():
    global camera_on
    camera_on = not camera_on
    if camera_on:
        camera_button.config(text="Turn Off Camera")
        show_camera_feed()
    else:
        camera_button.config(text="Turn On Camera")
        canvas.itemconfig(video_stream, image="")

# Function to show camera feed


def show_camera_feed():
    global arduino  # Add this line to use the global arduino object
    if camera_on:
        _, frame = cap.read()

        x, y, c = frame.shape

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = hands.process(framergb)

        className = ''

        # post process the result
        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)
                    landmarks.append([lmx, lmy])

                # Drawing landmarks on frames
                mpDraw.draw_landmarks(
                    frame, handslms, mpHands.HAND_CONNECTIONS)

                # Predict gesture
                prediction = model.predict([landmarks])
                classID = np.argmax(prediction)
                className = classNames[classID]

                # Control Arduino based on recognized gesture
                print("Before serial write")
                try:
                    if className == 'okay':
                        arduino.write(b'OKAY\n')  # Turn on all components
                    elif className == "stop":
                        arduino.write(b'STOP\n')  # Turn off all components
                    elif className == 'smile':
                        arduino.write(b'SMILE\n')  # Turn on 1st socket
                    elif className == 'live long':
                        arduino.write(b'LIVE_LONG\n')  # Turn off 1st socket
                    elif className == 'thumbs up':
                        arduino.write(b'THUMBS_UP\n')  # Turn on 2nd socket
                    elif className == 'thumbs down':
                        arduino.write(b'THUMBS_DOWN\n')  # Turn off 2nd socket
                    elif className == 'peace':
                        arduino.write(b'PEACE\n')  # Turn on bulb 
                    elif className == 'call me':
                        arduino.write(b'CALL_ME\n')  # Turn off bulb
                    elif className == 'fist':
                        arduino.write(b'FIST\n')  # Turn On the Buzzer
                    elif className == 'rock':
                        arduino.write(b'ROCK\n')  # Turn Off the Buzzer
                    print("After serial write") 
                except serial.SerialException as e:
                    print(f"Serial communication error: {e}")

        # Convert the frame to RGB format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert the frame to ImageTk format
        image = Image.fromarray(frame_rgb)
        photo = ImageTk.PhotoImage(image=image)

        # Update the canvas with the new frame
        canvas.itemconfig(video_stream, image=photo)
        canvas.image = photo

        # Continue showing camera feed
        root.after(10, show_camera_feed)


# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize GUI
root = tk.Tk()
root.title("Gesture Control & Speech Recognition")
root.geometry("800x600")

# Initialize variables for toggling features
speech_recognition_on = False
camera_on = False

# Create buttons
speech_button = tk.Button(
    root, text="Turn On Speech Recognition", command=toggle_speech_recognition)
speech_button.pack(pady=10)

camera_button = tk.Button(root, text="Turn On Camera", command=toggle_camera)
camera_button.pack(pady=10)

# Create canvas for displaying camera feed
canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()

# Create placeholder for video stream
video_stream = canvas.create_image(0, 0, anchor=tk.NW)

# Start the GUI event loop
root.mainloop()

# Release the webcam and close the serial connection when GUI is closed
def cleanup():
    global arduino
    if 'arduino' in globals():  # Check if arduino is defined before closing
        try:
            arduino.close()
        except serial.SerialException as e:
            print(f"Error closing serial connection: {e}")
    cv2.destroyAllWindows()

root.protocol("WM_DELETE_WINDOW", cleanup)  # Call cleanup when closing the window
