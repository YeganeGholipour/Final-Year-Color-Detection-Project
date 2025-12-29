# Import necessary libraries
from color_detection_main_version.color_detection_calss import ColorDetector
import time
import cv2


# =========================
# Simulation configuration
# =========================
SCAN_START = 10
SCAN_END = 1700
SCAN_STEP = 10

GRAB_HOLD_TIME = 3  # seconds

# =========================
# Initialization
# =========================
print("Simulating port connection...")
print("Simulating correct Dynamixel settings...")

current_position = SCAN_START

detector = ColorDetector()

cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)

try:
    while current_position < SCAN_END:
        # ---- Simulate motor movement ----
        current_position += SCAN_STEP
        print(f"Simulating movement: Current position: {current_position}")

        # ---- Read camera frame ----
        ret, frame = detector.cap.read()
        if not ret:
            raise RuntimeError("Failed to read frame from camera")

        # ---- ROI calculation ----
        roi, x1, y1 = detector.calculate_roi(frame)

        if roi is None or roi.size == 0:
            print("Invalid ROI detected, skipping frame...")
            cv2.imshow("Camera Feed", frame)
            cv2.waitKey(1)
            continue

        # ---- Processing ----
        detector.draw_rectangle(roi, x1, y1, frame)
        hsv_roi = detector.transform_to_hsv(roi)

        blue_count, green_count, red_count = detector.calculate_bounds(hsv_roi)
        color = detector.show_color(
            blue_count,
            green_count,
            red_count,
            x1,
            y1,
            frame
        )

        # ---- Display ----
        cv2.imshow("Camera Feed", frame)
        cv2.waitKey(1)

        # ---- Action logic ----
        if color == "Blue":
            print("Detected Color: Blue")
            print("Simulating Dynamixel motor (ID=1): 1500")
            print("Simulating gripper motor (ID=12): 18000")

            time.sleep(GRAB_HOLD_TIME)
            break

    print("Scan finished or object detected. Stopping...")

finally:
    # =========================
    # Cleanup
    # =========================
    if detector.cap.isOpened():
        detector.cap.release()

    cv2.destroyAllWindows()
    print("Simulation complete. Port closed (simulated).")
