# Final-Year-Color-Detection-Project

Dynamixel Servo Motor Arm For Color Detection

This project uses the Dynamixel Servo Motor, Arm Robot for detecting objects based on a given pattern.

## Functionality:

- The robot scans all objects in a line from start_point to stop_point.
- Whenever it detects an object with a certain color, it enables the gripper motor and grabs the object.

### test.py file

#### Functionality:

- Simulates communication with Dynamixel servos (not actual communication)
- Scans from left to right and right to left
- Detects blue objects (simulated through a ColorDetector class)
- Simulates grabbing detected blue objects

#### Notes:

- This is a simulation and does not communicate with real Dynamixel servos.
- The `color_detection_calss.py` file is a placeholder and needs to be implemented based on your chosen color detection method.

## Requirements:

- Python 3.x

## Installation:

No installation is required for this simulation.

## Usage:

1. Clone or download this repository.
2. Open a terminal or command prompt and navigate to the project directory.
3. Run the simulation script: `test.py`
4. Press any key when prompted to initiate the scan.
5. The simulation will run until a blue object is detected or the scan path is complete.
6. Press any key again to restart the simulation.

## Code Structure:

- `test.py`: Main simulation script.
- `color_detection_calss.py` (placeholder): Simulates color detection logic (replace with your actual color detection implementation).
- The main file: `read_write.py`
