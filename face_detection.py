from __future__ import print_function
import sys
import cv2
import numpy as np
import serial
from random import randint

# def preprocess(action_frame):

#     blur = cv2.GaussianBlur(action_frame, (3,3), 0)
#     hsv = cv2.cvtColor(blur, cv2.COLOR_RGB2HSV)

#     lower_color = np.array([108, 23, 82])
#     upper_color = np.array([179, 255, 255])

#     mask = cv2.inRange(hsv, lower_color, upper_color)
#     blur = cv2.medianBlur(mask, 5)

#     kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
#     hsv_d = cv2.dilate(blur, kernel)

#     # hsv_d = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel)

#     return hsv_d

# # To account for eyes opening and closing, we can find the eye-aspect ratio
# def eye_aspect_ratio(eye):
#     """Calculate the aspect ratio of an eye region."""
#     # Compute the euclidean distances between the two sets of
#     # vertical eye landmarks (x, y)-coordinates
#     A = np.linalg.norm(eye[1] - eye[5])
#     B = np.linalg.norm(eye[2] - eye[4])
#     # Compute the euclidean distance between the horizontal
#     # eye landmark (x, y)-coordinates
#     C = np.linalg.norm(eye[0] - eye[3])
#     # Compute the eye aspect ratio
#     ear = (A + B) / (2.0 * C)
#     # Return the eye aspect ratio
#     return ear
        
# Initialize video capture
cap = cv2.VideoCapture(0)

# Set our dimensions for the ROI
roi_x = 650
roi_y = 200
roi_w = 600
roi_h = 600

FACE_THRESHOLD = 200
# EYE_OPEN_THRESHOLD = 0.3
# EYE_CLOSE_THRESHOLD = 0.6

# # Define the color range to track in HSV
# lower_color = np.array([108, 23, 82], dtype = "uint8")  # Lower HSV range for the object color
# upper_color = np.array([179, 255, 255], dtype = "uint8")  # Upper HSV range for the object color


# Read subsequent frames
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
    faces = face_cascade.detectMultiScale(frame, 1.3, 5, minSize=(40, 40))

    if not any(map(len, faces)):
        print("Face has crossed the threshold!")
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, 'Look Out!', (10,450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)

    else:
        # Draw bounding boxes around the detected contours
        for (x,y,w,h) in faces:
            # x, y, w, h = cv2.boundingRect(face)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Calculate the center of the face
            face_center_x = x + w // 2
            face_center_y = y + h // 2

            # Calculate the center of the ROI
            roi_center_x = roi_x + roi_w // 2
            roi_center_y = roi_y + roi_h // 2

            # Calculate the distance between the face center and the ROI center
            distance = ((face_center_x - roi_center_x) ** 2 + (face_center_y - roi_center_y) ** 2) ** 0.5

            # Check if the face has passed the threshold
            if (distance > FACE_THRESHOLD):
                # Do something when the face passes the threshold (e.g., print a message)
                print("Face has crossed the threshold!")
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, 'Look Out!', (10,450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)


                # These are causing errors (probably b/c we don't have anything connected).
                # ser = serial.Serial('/dev/ttyACM0', 9600)
                # ser.write(b'SIGNAL') 
                # ser.close()

            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

                # # Extract eye region
                # eye_region = roi_gray[ey:ey+eh, ex:ex+ew]

                # # Calculate aspect ratio of the eye
                # eye_aspect_ratio_value = eye_aspect_ratio([[ex, ey], [ex+ew//2, ey], [ex+ew, ey+eh//2], [ex+ew//2, ey+eh], [ex, ey+eh//2], [ex+ew, ey+eh//2]])

                # if eye_aspect_ratio_value < EYE_CLOSE_THRESHOLD:
                #     print("Eyes Closed!")

                # if eye_aspect_ratio_value > EYE_OPEN_THRESHOLD:
                #     print("Eyes open!")


    # Draw the ROI frame
    cv2.rectangle(frame, (roi_x, roi_y), (roi_x+roi_w, roi_y+roi_h), (0, 255, 0), 2)


    # Display the resulting frame
    cv2.imshow('Object Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()
