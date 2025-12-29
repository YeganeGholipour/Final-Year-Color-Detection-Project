import os
import time
import cv2
import socket
import pickle
from dynamixel_sdk import *

# Check platform and set getch function for user input
if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# Initialize Dynamixel SDK constants and variables
ADDR_MX_TORQUE_ENABLE = 24
ADDR_MX_GOAL_POSITION = 30
ADDR_MX_PRESENT_POSITION = 36
ADDR_MOVING_SPEED = 32

PROTOCOL_VERSION = 1.0
DXL_ID = 4
BAUDRATE = 57600
DEVICENAME = '/dev/tty0'

TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
DXL_MINIMUM_POSITION_VALUE = 10
DXL_MAXIMUM_POSITION_VALUE = 4000
DXL_MOVING_STATUS_THRESHOLD = 20

index = 0
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

# Set baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Enable Dynamixel torque and set initial positions
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_MOVING_SPEED, 50)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 1, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 1, ADDR_MX_GOAL_POSITION, 2000)
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 12, ADDR_MX_GOAL_POSITION, 24000)

if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully connected")

# Socket setup for receiving color detection messages
port = 12345
s = socket.socket()
s.bind(('192.168.1.100', port))
s.listen(5)
print("Waiting for connection from the client...")
client, addr = s.accept()
print("Connected to client at address:", addr)

try:
    while True:
        print("Press any key to continue! (or press ESC to quit!)")

        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_MX_GOAL_POSITION, dxl_goal_position[index])

        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        # Get user input for color orders
        color_order = input("Please enter the color order: ")
        colors = []
        for color in color_order.lower().split():
            colors.append(color)

        for color in colors:
            while True:
                # Read present position
                dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, ADDR_MX_PRESENT_POSITION)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error))

                print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID, dxl_goal_position[index], dxl_present_position))

                # Check if goal position is not reached
                if abs(dxl_goal_position[index] - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
                    try:
                        m = pickle.dumps(["salam"])
                        # Check for messages from the client
                        mes = client.recv(1024)
                        if mes:
                            message = pickle.loads(mes)
                            if message == [color]:
                                print(f"Detected Color is {color}")
                                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 1, ADDR_MX_GOAL_POSITION, 1500)
                                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 12, ADDR_MX_GOAL_POSITION, 18000)
                                # pick and place
                                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 1, ADDR_MX_GOAL_POSITION, 1200)
                                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 12, ADDR_MX_GOAL_POSITION, 20000)
                                
                                time.sleep(3)
                                break
                    except Exception as e:
                        print("Error receiving data:", e)

                    cv2.waitKey(1)

                else:
                    print("Goal position reached. Stopping...")
                    break

        print("Scanning complete.")

        if index == 0:
            index = 1
        else:
            index = 0

except KeyboardInterrupt:
    print("Terminating...")

finally:
    # Close socket connection
    client.close()
    s.close()

    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    portHandler.closePort()
