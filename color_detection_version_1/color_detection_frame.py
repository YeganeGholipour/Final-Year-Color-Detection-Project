# Multiple Objects At The Same Time
# ROI is the whole Frame

import cv2
import numpy as np

# Capture video from the camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    
    if not ret:
        break

    # Define the region of interest (e.g., the entire frame)
    roi = frame
    
    # Convert the region of interest to the HSV color space
    hsv_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # Define the lower and upper bounds of BLUE
    blue_lower_bound = np.array([100, 100, 100])  
    blue_upper_bound = np.array([140, 255, 255]) 
    
    # Threshold the HSV image to isolate BLUE
    blue_mask = cv2.inRange(hsv_frame, blue_lower_bound, blue_upper_bound)

    # Define the lower and upper bounds of GREEN
    green_lower_bound = np.array([40, 100, 100])
    green_upper_bound = np.array([80, 255, 255])

    # Threshold the HSV image to isolate GREEN
    green_mask = cv2.inRange(hsv_frame, green_lower_bound, green_upper_bound)

    # Define the lower and upper bounds of BLUE
    red_lower_bound = np.array([170, 100, 100])
    red_upper_bound = np.array([180, 255, 255])

    # Threshold the HSV image to isolate RED
    red_mask = cv2.inRange(hsv_frame, red_lower_bound, red_upper_bound)
    
    # Find contours for BLUE
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Iterate through the BLUE contours and draw them on the original frame
    for blue_contour in blue_contours:
        cv2.drawContours(frame, [blue_contour], -1, (255, 0, 0), 2)
        cv2.putText(frame, "Blue Colour", (0, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX,  
                        1.0, (255, 0, 0))

    # Find contours for GREEN
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Iterate through the GREEN contours and draw them on the original frame
    for green_contour in green_contours:
        cv2.drawContours(frame, [green_contour], -1, (0, 255, 0), 2)
        cv2.putText(frame, "Green Colour", (0, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX,  
                        1.0, (0, 255, 0))

    # Find contours for RED
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Iterate through the RED contours and draw them on the original frame
    for red_contour in red_contours:
        cv2.drawContours(frame, [red_contour], -1, (0, 0, 255), 2)
        cv2.putText(frame, "Red Colour", (0, 150), 
                        cv2.FONT_HERSHEY_SIMPLEX,  
                        1.0, (0, 0, 255))

    
    # Display the original frame with contours
    cv2.imshow('Color Detection', frame)
    
    # Check for key press and break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
