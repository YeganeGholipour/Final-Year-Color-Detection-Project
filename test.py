# Import necessary libraries
from color_detection_calss import ColorDetector
import time

# Simulate port connection
print("Simulating port connection...")

# Dynamixel settings (placeholder for real configuration)
print("Simulating correct Dynamixel settings...")

# Define goal position and movement increment
GOAL_POSITION = 700
MOVEMENT_INCREMENT = 10  # Adjust this for desired scanning speed

# Initialize current position
current_position = 10  # Change this to the starting position

# Create an instance of ColorDetector outside the loop
detector = ColorDetector()
while True:
    print("Press any key to continue...")
    input()  # Wait for user input to simulate user interaction

    # Simulate movement towards goal position
    while current_position != GOAL_POSITION:
        if current_position < GOAL_POSITION:
            current_position += MOVEMENT_INCREMENT
        else:
            current_position -= MOVEMENT_INCREMENT

        print(f"Simulating movement: Current position: {current_position}")

        # Simulate object detection
        detector.capture()
        detected_color = detector.show_color()

        # Inside the object detection loop
        print("Detected color:", detected_color)  # Print the detected color    

        if detected_color == "Blue":
            print("Blue object detected!")

            # Simulate grabbing action (print desired motor positions)
            print("Simulating Dynamixel motor (ID=1): 1500")
            print("Simulating gripper motor (ID=12): 18000")
            time.sleep(3)  # Simulate holding time
            break  # Exit inner loop if object is grabbed

        # No blue object detected, continue scanning
        print("No blue object detected, continuing scan...")

    # Reached end of scan path, reverse direction
    GOAL_POSITION = 2000 if GOAL_POSITION == 700 else 700  # Swap goal position

print("Simulation complete. Port closed (simulated).")
