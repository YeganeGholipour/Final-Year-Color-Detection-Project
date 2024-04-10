import os


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


ADDR_PRO_TORQUE_ENABLE      = 64               
ADDR_PRO_GOAL_POSITION      = 116
ADDR_PRO_PRESENT_POSITION   = 132

ADDR_MX_TORQUE_ENABLE      = 24               
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36

PROTOCOL_VERSION            = 2.0               


DXL_ID                      = 1                 
BAUDRATE                    = 57600             
DEVICENAME                  = '/dev/tty0'    
                                                

TORQUE_ENABLE               = 1                 
TORQUE_DISABLE              = 0                 
DXL_START_POSITION_VALUE = 10
DXL_STOP_POSITION_VALUE = 200           
DXL_MOVING_STATUS_THRESHOLD = 20                

     
grip_goal_position = [18000, 28000]

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


dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS: 
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0: 
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully connected")

# initialize the color detection
detector = ColorDetector()

# writting
while True:
    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(0x1b):
        break

    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PRO_GOAL_POSITION, DXL_STOP_POSITION_VALUE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    # reading
    while True:
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRO_PRESENT_POSITION)
        blue, _, _ = detector.calculate_bounds()
        max_count = detector.show_color()
        if max_count == blue:
            print('Blue object detected')

            while True:
                dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 12, ADDR_MX_GOAL_POSITION, grip_goal_position[1])   
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error))


        if not abs(DXL_STOP_POSITION_VALUE - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
            print('The robot has reached the end point And has not found a blue object')
            break


dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))


portHandler.closePort()
