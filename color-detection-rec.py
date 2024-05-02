# Multiple Objects At The Same Time
# ROI is a Rectangle


import cv2
import numpy as np

# Capture video from the camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    
    if not ret:
        break

    # Calculate the dimensions of the ROI rectangle
    height, width = frame.shape[:2]
    roi_width, roi_height = int(width * 0.5), int(height * 0.5)
    roi_x = int((width - roi_width) / 2)
    roi_y = int((height - roi_height) / 2)

    # Define the region of interest (rectangle in the center of the frame)
    roi = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
    
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
        cv2.putText(frame, "Green Colour", (0, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX,  
                        1.0, (0, 255, 0))

    # Find contours for RED
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Iterate through the RED contours and draw them on the original frame
    for red_contour in red_contours:
        cv2.drawContours(frame, [red_contour], -1, (0, 0, 255), 2)
        cv2.putText(frame, "Red Colour", (0, 50), 
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




# One Object
# ROI is a rectangle

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

rect_width = 200
rect_height = 200
rect_color = (255, 255, 255)
rect_thickness = 2

x1 = int((frame_width - rect_width) / 2)
y1 = int((frame_height - rect_height) / 2)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    cv2.rectangle(frame, (x1, y1), (x1 + rect_width, y1 + rect_height), rect_color, rect_thickness)

    roi = frame[y1: y1 + rect_height, x1:x1 + rect_width]

    hsv_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    blue_lower_bound = np.array([100, 100, 100])
    blue_upper_bound = np.array([140, 255, 255])

    green_lower_bound = np.array([40, 100, 100])
    green_upper_bound = np.array([80, 255, 255])

    red_lower_bound1 = np.array([0, 100, 100])
    red_upper_bound1 = np.array([10, 255, 255])

    red_lower_bound2 = np.array([160, 100, 100])
    red_upper_bound2 = np.array([180, 255, 255])

    mask_blue = cv2.inRange(hsv_frame, blue_lower_bound, blue_upper_bound)
    mask_green = cv2.inRange(hsv_frame, green_lower_bound, green_upper_bound)
    mask_red1 = cv2.inRange(hsv_frame, red_lower_bound1, red_upper_bound1)
    mask_red2 = cv2.inRange(hsv_frame, red_lower_bound2, red_upper_bound2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    blue_contour_count = len(contours_blue)
    green_contour_count = len(contours_green)
    red_contour_count = len(contours_red)

    max_contour_count = max(blue_contour_count, green_contour_count, red_contour_count)

    if max_contour_count == blue_contour_count:
        color = "Blue"
        cv2.putText(frame, color, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    elif max_contour_count == green_contour_count:
        color = "Green"
        cv2.putText(frame, color, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    else:
        color = "Red"
        cv2.putText(frame, color, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    

    cv2.imshow('Color Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()