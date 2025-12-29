import cv2
import numpy as np

class ColorDetector:
    def __init__(self):
        self.rect_color = (255, 255, 255)
        self.rect_thickness = 2

        self.cap = cv2.VideoCapture(0)
        
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        self.rect_width = 200
        self.rect_height = 200

    @property
    def rectangle_width(self):
        return self.rect_width
        
    @rectangle_width.setter    
    def rectangle_width(self, value):
        self.rect_width = value

    @property
    def rectangle_height(self):
        return self.rect_height
        
    @rectangle_height.setter    
    def rectangle_height(self, value):
        self.rect_height = value

    def calculate_roi(self, frame):
        x1 = int((self.frame_width - self.rect_width) / 2)
        y1 = int((self.frame_height - self.rect_height) / 2)
        roi = frame[y1: y1 + self.rect_height, x1:x1 + self.rect_width]
        return (roi, x1, y1)

    def draw_rectangle(self, roi, x1, y1, frame):
        cv2.rectangle(frame, (x1, y1), (x1 + self.rect_width, y1 + self.rect_height), self.rect_color, self.rect_thickness)

    def transform_to_hsv(self, roi):
        hsv_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        return hsv_frame

    def calculate_bounds(self, hsv_frame):
        blue_lower_bound = np.array([100, 219, 226])
        blue_upper_bound = np.array([124, 255, 255])
    
        green_lower_bound = np.array([40, 40, 40])
        green_upper_bound = np.array([70, 255, 255])
    
        red_lower_bound1 = np.array([0, 50, 70])
        red_upper_bound1 = np.array([10, 255, 255])

        red_lower_bound2 = np.array([170, 50, 70])
        red_upper_bound2 = np.array([180, 255, 255])
    
        yellow_lower_bound = np.array([20, 100, 100])
        yellow_upper_bound = np.array([30, 255, 255])

        orange_lower_bound = np.array([10, 100, 20])
        orange_upper_bound = np.array([25, 255, 255])

        purple_lower_bound = np.array([130, 50, 70])
        purple_upper_bound = np.array([160, 255, 255])

        pink_lower_bound = np.array([140, 50, 75])
        pink_upper_bound = np.array([170, 255, 255])

        mask_blue = cv2.inRange(hsv_frame, blue_lower_bound, blue_upper_bound)
        mask_green = cv2.inRange(hsv_frame, green_lower_bound, green_upper_bound)
        mask_yellow = cv2.inRange(hsv_frame, yellow_lower_bound, yellow_upper_bound)
        mask_orange = cv2.inRange(hsv_frame, orange_lower_bound, orange_upper_bound)
        mask_purple = cv2.inRange(hsv_frame, purple_lower_bound, purple_upper_bound)
        mask_pink = cv2.inRange(hsv_frame, pink_lower_bound, pink_upper_bound)
        mask_red1 = cv2.inRange(hsv_frame, red_lower_bound1, red_upper_bound1)
        mask_red2 = cv2.inRange(hsv_frame, red_lower_bound2, red_upper_bound2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)

        # Apply Gaussian Blur
        mask_blue = cv2.GaussianBlur(mask_blue, (5, 5), 0)
        mask_green = cv2.GaussianBlur(mask_green, (5, 5), 0)
        mask_red = cv2.GaussianBlur(mask_red, (5, 5), 0)
        mask_yellow = cv2.GaussianBlur(mask_yellow, (5, 5), 0)
        mask_orange = cv2.GaussianBlur(mask_orange, (5, 5), 0)
        mask_purple = cv2.GaussianBlur(mask_purple, (5, 5), 0)
        mask_pink = cv2.GaussianBlur(mask_pink, (5, 5), 0)

        # Apply morphological operations
        kernel = np.ones((5, 5), np.uint8)
        mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_CLOSE, kernel)
        mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)
        mask_yellow = cv2.morphologyEx(mask_yellow, cv2.MORPH_CLOSE, kernel)
        mask_orange = cv2.morphologyEx(mask_orange, cv2.MORPH_CLOSE, kernel)
        mask_purple = cv2.morphologyEx(mask_purple, cv2.MORPH_CLOSE, kernel)
        mask_pink = cv2.morphologyEx(mask_pink, cv2.MORPH_CLOSE, kernel)

        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_orange, _ = cv2.findContours(mask_orange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_purple, _ = cv2.findContours(mask_purple, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_pink, _ = cv2.findContours(mask_pink, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        blue_area = sum(cv2.contourArea(contour) for contour in contours_blue)
        green_area = sum(cv2.contourArea(contour) for contour in contours_green)
        red_area = sum(cv2.contourArea(contour) for contour in contours_red)

        yellow_area = sum(cv2.contourArea(contour) for contour in contours_yellow)
        orange_area = sum(cv2.contourArea(contour) for contour in contours_orange)
        purple_area = sum(cv2.contourArea(contour) for contour in contours_purple)
        pink_area = sum(cv2.contourArea(contour) for contour in contours_pink)

        return (blue_area, green_area, red_area, yellow_area, orange_area, purple_area, pink_area)

    def show_color(self, blue_area, green_area, red_area, yellow_area, orange_area, purple_area, pink_area, x1, y1, frame):
        max_area = max(blue_area, green_area, red_area, yellow_area, orange_area, purple_area, pink_area)
        
        if max_area == blue_area:
            color = "Blue"
            cv2.putText(frame, color, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        
        elif max_area == green_area:
            color = "Green"
            cv2.putText(frame, color, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        elif max_area == red_area:
            color = "Red"
            cv2.putText(frame, color, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        elif max_area == yellow_area:
            color = "Yellow"
            cv2.putText(frame, color, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
        
        elif max_area == orange_area:
            color = "Orange"
            cv2.putText(frame, color, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 153, 0), 2)
        
        elif max_area == purple_area:
            color = "Purple"
            cv2.putText(frame, color, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (153, 51, 153), 2)
        
        elif max_area == pink_area:
            color = "Pink"
            cv2.putText(frame, color, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 153, 255), 2)

        return color

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            roi, x1, y1 = self.calculate_roi(frame)
            self.draw_rectangle(roi, x1, y1, frame)
            hsv_frame = self.transform_to_hsv(roi)
            blue_area, green_area, red_area, yellow_area, orange_area, purple_area, pink_area = self.calculate_bounds(hsv_frame)
            detected_color = self.show_color(blue_area, green_area, red_area, yellow_area, orange_area, purple_area, pink_area, x1, y1, frame)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    color_detector = ColorDetector()
    color_detector.run()