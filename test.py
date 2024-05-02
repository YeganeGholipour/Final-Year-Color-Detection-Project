# Import necessary libraries
from color_detection_calss import ColorDetector
import time
import cv2

# Simulate port connection
print("Simulating port connection...")

# Dynamixel settings (placeholder for real configuration)
print("Simulating correct Dynamixel settings...")

# Define goal position and movement increment
GOAL_POSITION = 1700
MOVEMENT_INCREMENT = 10  # Adjust this for desired scanning speed

# Initialize current position
current_position = 10  # Change this to the starting position

# Create an instance of ColorDetector outside the loop
detector = ColorDetector()
cv2.namedWindow("Camera Feed")  # Create a named window for displaying camera feed

try:
    while True:
        # Simulate movement towards goal position
        if current_position < GOAL_POSITION:
            current_position += MOVEMENT_INCREMENT
            print(f"Simulating movement: Current position: {current_position}")

            ret, frame = detector.cap.read()
            if not ret:
                break

            roi, x1, y1 = detector.calculate_roi(frame)
            detector.draw_rectangle(roi, x1, y1, frame)
            hsv_frame = detector.transform_to_hsv(roi)

            blue_count, green_count, red_count = detector.calculate_bounds(hsv_frame)
            color = detector.show_color(blue_count, green_count, red_count, x1, y1, frame)
            # cv2.putText(frame, color, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            cv2.imshow("Camera Feed", frame)  # Display camera feed

            if color == "Blue":
                print("Detected Color is Blue")
                # Simulate grabbing action (print desired motor positions)
                print("Simulating Dynamixel motor (ID=1): 1500")
                print("Simulating gripper motor (ID=12): 18000")
                time.sleep(3)  # Simulate holding time
                break  # Exit inner loop if object is grabbed

            cv2.waitKey(1)  # Required to refresh imshow window

        # Check if goal position is reached
        elif current_position >= GOAL_POSITION:
            print("Goal position reached. Stopping...")
            break

finally:
    # Release resources
    detector.cap.release()
    cv2.destroyAllWindows()
    print("Simulation complete. Port closed (simulated).")
