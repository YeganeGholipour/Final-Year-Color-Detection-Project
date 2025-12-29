import tkinter as tk
from tkinter import *
import socket
import pickle
from color_detection_main_version.color_detection_calss import ColorDetector
import cv2

####### Screen Setting #######
screen = Tk()
screen.geometry('800x900')
screen.configure(bg = '#000000')
screen.resizable(0, 0)
screen.title("Color Detector Robot")

###### Functions ##############
def start():
    port = 12345
    port1=12346	
    s = socket.socket()		
    s.connect(('192.168.1.100', port)) 
    s1=socket.socket()	
    s1.bind(('192.168.1.102',port1))
    s1.listen(5)
    client,addr = s1.accept()
    initial_info=s.recv(1024)

    first_color = first_color_text.get()
    second_color = second_color_text.get()
    third_color = third_color_text.get()

    detector = ColorDetector()  
    color_list = [first_color, second_color, third_color]

    m=pickle.loads(initial_info)
    if m==['salam']:
        for target_color in color_list:
            while True:
                ret, frame = detector.cap.read()
                if not ret:
                    break

                roi, x1, y1 = detector.calculate_roi(frame)
                detector.draw_rectangle(roi, x1, y1, frame)
                hsv_frame = detector.transform_to_hsv(roi)

                blue_count, green_count, red_count = detector.calculate_bounds(hsv_frame)
                detected_color = detector.show_color(blue_count, green_count, red_count, x1, y1, frame)

                cv2.imshow("Color Detection", frame)

                if detected_color == target_color:
                    mes=pickle.dumps([detected_color])
                    client.send(mes)
                    print(f"Detected Color is {detected_color}")
                    detection_lbl["text"] = f"Detected Color is {detected_color}"
                    break  

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    detector.cap.release()
                    cv2.destroyAllWindows()
                    return

        detector.cap.release()
        cv2.destroyAllWindows()
    else:
        print("not connected")

####### Labels ################
first_color_lbl = Label(screen, text="Enter the first color", font="thahoma 15", fg="#FFFF69", bg='#000000')
first_color_lbl.pack(pady=10)

first_color_text = StringVar()
first_color_entry = Entry(screen, textvariable=first_color_text, bg='#CDCDB7')
first_color_entry.pack(pady=10)
#####
second_color_lbl = Label(screen, text="Enter the second color", font="thahoma 15", fg="#FFFF69", bg='#000000')
second_color_lbl.pack(pady=10)

second_color_text = StringVar()
second_color_entry = Entry(screen, textvariable=second_color_text, bg='#CDCDB7')
second_color_entry.pack(pady=10)
####
third_color_lbl = Label(screen, text="Enter the third color", font="thahoma 15", fg="#FFFF69", bg='#000000')
third_color_lbl.pack(pady=10)

third_color_text = StringVar()
third_color_entry = Entry(screen, textvariable=third_color_text, bg='#CDCDB7')
third_color_entry.pack(pady=10)
####
detection_lbl = Label(screen, text="", font="thahoma 15", fg="#FFFF69", bg='#000000')
detection_lbl.pack(pady=10)

#### Buttons #####
start_btn = Button(screen, text='Start', width=12, cursor="hand1", command=start, bg="#FFFF69", fg="black", activebackground='deep pink', font="thahoma 15")
start_btn.pack(pady=10)

screen.mainloop()