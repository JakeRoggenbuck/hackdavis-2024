from __future__ import print_function
import sys
import cv2
import numpy as np
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

# First define an individual tracker
# tracker_types = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

# def makeTracker(tracker_type):
#     if tracker_type == tracker_types[0]:
#         tracker = cv2.TrackerBoosting_create()
#     elif tracker_type == tracker_types[1]:
#         tracker = cv2.TrackerMIL_create()
#     elif tracker_type == tracker_types[2]:
#         tracker = cv2.TrackerKCF_create()
#     elif tracker_type == tracker_types[3]:
#         tracker = cv2.TrackerTLD_create()
#     elif tracker_type == tracker_types[4]:
#         tracker = cv2.TrackerMEDIANFLOW_create()
#     elif tracker_type == tracker_types[5]:
#         tracker = cv2.TrackerGOTURN_create()
#     elif tracker_type == tracker_types[6]:
#         tracker = cv2.TrackerMOSSE_create()
#     elif tracker_type == tracker_types[7]: 
#         tracker = cv2.TrackerCSRT_create()
#     else:
#         tracker = None
#         print('Incorrect tracker name')
#         print('Available trackers are:')
#         for t in tracker_types:
#             print(t)
    
#     return tracker
        

# Initialize video capture
cap = cv2.VideoCapture(0)

# Set our dimensions for the ROI
roi_x = 500
roi_y = 500
roi_w = 800
roi_h = 600

threshold = 300

# # Define the color range to track in HSV
# lower_color = np.array([108, 23, 82], dtype = "uint8")  # Lower HSV range for the object color
# upper_color = np.array([179, 255, 255], dtype = "uint8")  # Upper HSV range for the object color

# Read the initial frame to initialize our boxes to track

# ret, frame = cap.read()
# if not ret:
#     sys.exit(1)

# boxes = []
# colors = []

# # Locate our objects in the first frame
# while True:
#     box = cv2.selectROI('MultiTracker', frame)
#     boxes.append(box)
#     colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
#     k = cv2.waitKey(0) & 0xFF
#     if (k == 113):  # q is pressed
#         break

# tracker_type = "CSRT"
# multi_tracker = cv2.MultiTracker_create()

# for box in boxes:
#     multi_tracker.add(makeTracker(tracker_type), frame, box)

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
        if distance > threshold:
            # Do something when the face passes the threshold (e.g., print a message)
            print("Face has crossed the threshold!")

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    # Draw the ROI frame
    cv2.rectangle(frame, (roi_x, roi_y), (roi_x+roi_w, roi_y+roi_h), (0, 255, 0), 2)


    # Display the resulting frame
    cv2.imshow('Object Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()
