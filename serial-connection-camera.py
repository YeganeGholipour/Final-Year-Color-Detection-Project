import socket
import pickle
import cv2
from color_detection_calss import ColorDetector

# The client (Computer) - Initiates connection to the robot
# *******************************************
port = 12345
s = socket.socket()
s.connect(('192.168.1.100', port))
# *******************************************

# The server (Computer) - Listens for connection from the robot
# *******************************************
port1 = 12346
s1 = socket.socket()
s1.bind(('192.168.1.102', port1))
# *******************************************

# The server listens for connection
s1.listen(5)
# The server accepts the connection from the client (robot)
client, addr = s1.accept()

# The client (Computer) receives the initial message from the robot
initial_info = s.recv(1024)

# The client (Computer) decodes the message
m = pickle.loads(initial_info)

# If the message is "salam" then the color detection starts
if m == ['salam']:
    detector = ColorDetector()
    while True:
        ret, frame = detector.cap.read()
        if not ret:
            break

        roi, x1, y1 = detector.calculate_roi(frame)
        detector.draw_rectangle(roi, x1, y1, frame)
        hsv_frame = detector.transform_to_hsv(roi)

        blue_count, green_count, red_count = detector.calculate_bounds(hsv_frame)
        color = detector.show_color(blue_count, green_count, red_count, x1, y1, frame)

        cv2.imshow("Color Detection", frame)

        if color == "Blue":
            # The client (Computer) sends a message to the robot if blue is detected
            mes = pickle.dumps(["blue"])
            client.send(mes)
            print("Detected Color is Blue")
        else:
            print("Detected Color is Not Blue")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    detector.cap.release()
    cv2.destroyAllWindows()
else:
    print("not connected")
