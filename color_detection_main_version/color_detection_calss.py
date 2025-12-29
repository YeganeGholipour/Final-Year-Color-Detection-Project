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

        return (blue_contour_count, green_contour_count, red_contour_count)


    def show_color(self, blue_contour_count, green_contour_count, red_contour_count, x1, y1, frame):
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
        
        return color


# Uncomment this part to see how the detection works
   
# detector = ColorDetector()  
# while True:
#     ret, frame = detector.cap.read()
#     if not ret:
#         break

#     roi, x1, y1 = detector.calculate_roi(frame)
#     detector.draw_rectangle(roi, x1, y1, frame)
#     hsv_frame = detector.transform_to_hsv(roi)

#     blue_count, green_count, red_count = detector.calculate_bounds(hsv_frame)
#     color = detector.show_color(blue_count, green_count, red_count, x1, y1, frame)

#     cv2.imshow("Color Detection", frame)

#     if color == "Blue":
#         print("Detected Color is Blue")
#     else:
#         print("Detected Color is Not Blue")
    
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# detector.cap.release()
# cv2.destroyAllWindows()
