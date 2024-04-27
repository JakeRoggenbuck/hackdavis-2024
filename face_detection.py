import cv2
import numpy as np

def preprocess(action_frame):

    blur = cv2.GaussianBlur(action_frame, (3,3), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_RGB2HSV)

    lower_color = np.array([108, 23, 82])
    upper_color = np.array([179, 255, 255])

    mask = cv2.inRange(hsv, lower_color, upper_color)
    blur = cv2.medianBlur(mask, 5)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
    hsv_d = cv2.dilate(blur, kernel)

    # hsv_d = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel)

    return hsv_d

# Initialize video capture
cap = cv2.VideoCapture(0)

# Define the color range to track in HSV
lower_color = np.array([108, 23, 82], dtype = "uint8")  # Lower HSV range for the object color
upper_color = np.array([179, 255, 255], dtype = "uint8")  # Upper HSV range for the object color

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # clean = preprocess(frame)

    # Grayscale for image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # contours, _ = cv2.findContours(preprocess(frame), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    faces = face_cascade.detectMultiScale(frame, 1.1, 5, minSize=(40, 40))

    # Draw bounding boxes around the detected contours
    for (x,y,w,h) in faces:
        # x, y, w, h = cv2.boundingRect(face)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    # Display the resulting frame
    cv2.imshow('Object Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()
