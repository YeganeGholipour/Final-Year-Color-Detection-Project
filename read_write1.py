import os
import time

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

from dynamixel_sdk import *                    
from color_detection_calss import ColorDetector   


ADDR_MX_TORQUE_ENABLE      = 24               
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36
ADDR_MOVING_SPEED          = 32

PROTOCOL_VERSION            = 1.0               

DXL_ID                      = 4             
BAUDRATE                    = 57600            
DEVICENAME                  = '/dev/tty0'   
                                                

TORQUE_ENABLE               = 1                
TORQUE_DISABLE              = 0                
DXL_MINIMUM_POSITION_VALUE  = 10         
DXL_MAXIMUM_POSITION_VALUE  = 4000          
DXL_MOVING_STATUS_THRESHOLD = 20              

index = 0
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]         

portHandler = PortHandler(DEVICENAME)


packetHandler = PacketHandler(PROTOCOL_VERSION)

if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()


dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_MOVING_SPEED, 50)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 1, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 1, ADDR_MX_GOAL_POSITION, 2000)
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 12, ADDR_MX_GOAL_POSITION, 24000)


detector = ColorDetector()


if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully connected")

while 1:
    print("Press any key to continue! (or press ESC to quit!)")

    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_MX_GOAL_POSITION, dxl_goal_position[index])
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    while 1:
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, ADDR_MX_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID, dxl_goal_position[index], dxl_present_position))

        if not abs(dxl_goal_position[index] - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
            while True:
                blue, _, _ = detector.calculate_bounds()
                max_count = detector.show_color()
                if max_count == blue:
                    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 1, ADDR_MX_GOAL_POSITION, 1500)
                    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 12, ADDR_MX_GOAL_POSITION, 18000)
                    time.sleep(3)
                    break
                else:
                    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 1, ADDR_MX_GOAL_POSITION, 2000)
                    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 12, ADDR_MX_GOAL_POSITION, 25800)
                    

    if index == 0:
        index = 1
    else:
        index = 0


if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

portHandler.closePort()
