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

    def calculate_roi(self):
        x1 = int((self.frame_width - self.rect_width) / 2)
        y1 = int((self.frame_height - self.rect_height) / 2)
        self.roi = self.frame[y1: y1 + self.rect_height, x1:x1 + self.rect_width]
        return (self.roi, x1, y1)

    def draw_rectangle(self):
        cv2.rectangle(self.frame, (self.x1, self.y1), (self.x1 + self.rect_width, self.y1 + self.rect_height), self.rect_color, self.rect_thickness)

    def transform_to_hsv(self):
        hsv_frame = cv2.cvtColor(self.roi, cv2.COLOR_BGR2HSV)
        return hsv_frame

    def calculate_bounds(self):
        blue_lower_bound = np.array([100, 100, 100])
        blue_upper_bound = np.array([140, 255, 255])
    
        green_lower_bound = np.array([40, 100, 100])
        green_upper_bound = np.array([80, 255, 255])
    
        red_lower_bound1 = np.array([0, 100, 100])
        red_upper_bound1 = np.array([10, 255, 255])
    
        red_lower_bound2 = np.array([160, 100, 100])
        red_upper_bound2 = np.array([180, 255, 255])

        mask_blue = cv2.inRange(self.hsv_frame, blue_lower_bound, blue_upper_bound)
        mask_green = cv2.inRange(self.hsv_frame, green_lower_bound, green_upper_bound)
        mask_red1 = cv2.inRange(self.hsv_frame, red_lower_bound1, red_upper_bound1)
        mask_red2 = cv2.inRange(self.hsv_frame, red_lower_bound2, red_upper_bound2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        self.blue_contour_count = len(contours_blue)
        self.green_contour_count = len(contours_green)
        self.red_contour_count = len(contours_red)

        return (self.blue_contour_count, self.green_contour_count, self.red_contour_count)


    def show_color(self):
        max_contour_count = max(self.blue_contour_count, self.green_contour_count, self.red_contour_count)
        
        if max_contour_count == self.blue_contour_count:
            color = "Blue"
            cv2.putText(self.frame, color, (self.x1, self.y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        
        elif max_contour_count == self.green_contour_count:
            color = "Green"
            cv2.putText(self.frame, color, (self.x1, self.y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        else:
            color = "Red"
            cv2.putText(self.frame, color, (self.x1, self.y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        
        return color
    
    def capture(self):
        while True:
            ret, self.frame = self.cap.read()
            if not ret:
                break
        
            self.roi, self.x1, self.y1 = self.calculate_roi()
            self.draw_rectangle()
        
            self.hsv_frame = self.transform_to_hsv()

            self.blue_contour_count, self.green_contour_count, self.red_contour_count = self.calculate_bounds()

            color = self.show_color()
            
            cv2.imshow('Color Detection', self.frame)
        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        
        self.cap.release()
        cv2.destroyAllWindows()


detector = ColorDetector()
detector.capture()
