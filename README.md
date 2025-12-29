# Final Year Color Detection Project with Dynamixel Servo Motor Arm


> This repository was lightly refactored post-graduation for clarity and reviewability.


## Abstract

This project implements a **vision-guided robotic pick-and-place system** using a Dynamixel-based servo motor arm. The system integrates **computer vision, serial communication, motor control, and GUI-based interaction** to detect objects by color and manipulate them autonomously. Due to hardware constraints, full execution requires physical access to the robotic arm; however, the repository focuses on the **control logic, system architecture, and perception pipeline**, which were the primary evaluation criteria of the project.

---
## Problem Statement

Designing an autonomous pick-and-place robotic system introduces multiple challenges:

- Identifying and controlling undocumented servo motor IDs
    
- Achieving reliable color detection under real-world noise
    
- Coordinating multiple motors with interdependent motion constraints
    
- Maintaining stability and repeatability in grasping and placing objects
    

The goal was to build a **functional end-to-end system**, not just isolated components.

---
## System Overview

The system consists of the following components:

- **Robotic Arm**: Dynamixel servo motor arm with gripper
    
- **Vision System**: Laptop camera used for color-based object detection
    
- **Communication**: Serial/socket-based communication between vision module and robot controller
    
- **Control Logic**: Python-based motor coordination and motion sequencing
    
- **User Interface**: GUI for configuring detection order and initiating tasks

---
## Hardware Dependency

This project is **hardware-dependent by design**.

> Full execution requires a Dynamixel servo motor arm.  
> Without hardware, the system cannot perform physical motion; however, the **architecture, control logic, perception pipeline, and communication mechanisms** are fully inspectable and were evaluated through on-device testing and oral defense.

---
## What Can Be Evaluated Without Hardware

- Motor coordination logic and sequencing
    
- Control flow for pick, place, and reset phases
    
- Color detection pipeline design
    
- Serial/socket communication architecture
    
- Error cases, limitations, and design decisions

---
## Technical Details

### 1. Motor Identification & Initialization

The robotic arm lacked labeled motor IDs. Motor identification was achieved through:

- Active probing using Dynamixel **ping** commands
    
- Manual validation via controlled motor actuation
    

A dedicated initialization routine configures **position and speed** for all motors before motion begins.

---
### 2. Vision-Based Color Detection

Initial color detection supported three base colors. This approach proved insufficiently robust, leading to an improved pipeline:

- Expanded color set (e.g., yellow, orange, pink)
    
- Gaussian Blur preprocessing
    
- Morphological operations (5×5 kernel)
    
- Contour analysis for dominant color selection
    

This significantly improved detection stability.

---
### 3. Motion Planning: Pick & Place

The arm’s motion was decomposed into **two independent phases**:

- **Pick phase**: Coordinated use of motors 1 and 12 (gripper)
    
- **Place phase**: Coordinated use of motors 3 and 12
    

Key challenges included:

- Interdependent motor constraints
    
- Speed tuning (final speed set to 50 for stability)
    
- Avoiding unintended interference between joints
    

The final motion sequence:

1. System initialization
    
2. Move to detection position
    
3. Detect object color
    
4. Pick object
    
5. Move to target location
    
6. Place object
    
7. Return to default position

---
### 4. Communication Architecture

Since the robot lacked an onboard camera:

- Vision processing runs on the laptop
    
- Results are transmitted via **socket/serial communication**
    
- Color detection is implemented as a **separate module**, integrated into the control loop

---
### 5. Graphical User Interface

A GUI built with **Tkinter** allows:

- User-defined color priority order
    
- Starting and monitoring robot execution
    
- Real-time feedback on detected colors

---
### 6. Testing & Simulation

- A `test.py`-based testing file simulates basic logic without hardware
    
- Simulation uses counters instead of physical motion
    
- While limited, it supports early-stage validation and debugging

---
## Challenges

### 1. Undocumented Hardware Configuration

The robotic arm did not provide any physical or software documentation identifying servo motor IDs. This made even basic motion control non-trivial.

**Approach:**  
Motor IDs were identified through active probing using Dynamixel `ping` commands and manual validation via controlled motor actuation.

---
## 2. Interdependent Motor Coordination

Early implementations attempted to control only a subset of motors for object manipulation. This resulted in limited range of motion and unstable behavior.

**Approach:**  
Through iterative testing, it became clear that **all motors must be initialized and speed-limited** to achieve stable motion. A uniform speed of 50 was selected to balance precision and responsiveness.

---
### 3. Vision Robustness Under Noise

Initial color detection based on three primary colors produced unreliable results under real lighting conditions.

**Approach:**  
The vision pipeline was refined by expanding the color set and introducing Gaussian blur and morphological operations before contour analysis.

---
### 4. Pick-and-Place Sequencing Complexity

The pick-and-place process involved tightly coupled motor sequences where small timing or ordering changes caused unintended interference between joints.

**Approach:**  
The motion was decomposed into two logically independent phases—**pick** and **place**—with clearly defined motor responsibilities for each.

---
### 5. Loop Instability and Non-Deterministic Behavior

Under repeated execution, the system occasionally failed to complete the `place` phase correctly, and gripper open/close actions were sometimes inconsistent.

**Status:**  
These issues could not be fully resolved within the project timeframe. The behavior is theoretically correct but exhibits instability in practice, likely due to timing, synchronization, or hardware feedback limitations.

---
### 6. Testing Without Hardware Access

Hardware access was not always available, limiting continuous testing.

**Approach:**  
A lightweight test and simulation file was created using counters to emulate robot behavior for early-stage logic validation.

---


















___
## Known Limitations

- Occasional instability in the `place` phase during repeated loop execution
    
- Gripper open/close inconsistencies under certain timing conditions
    
- Full functional refactor was not hardware-validated due to access limitations
    

These issues were discussed during evaluation and reflect **real-world robotic system constraints**, not conceptual flaws.

---
## Code Structure 

- `color_detection_main_version`: color detection logic for 3 colors + multi colors
- `robot_mechanisms_main_version`: logic for both the movement of the arm + detecting color as it moves
- `graphical_user_interface`: the `tkinter` logic for connecting to the camera + `GUI` for the user to add the color priorities
- `communication`: logic for connecting to the laptop's camera

---
## Technologies Used

- Python
    
- Dynamixel SDK
    
- OpenCV
    
- Tkinter
    
- Socket / Serial Communication

---
## Evaluation Context

This project was assessed primarily through:

- System implementation
    
- Hardware testing
    
- Technical reasoning
    
- Oral defense
    

A full written dissertation was **not required**.  
Final grade awarded: **20/20**.

---
