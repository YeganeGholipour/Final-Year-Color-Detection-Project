
import os

def port_hand_po(porthandler,DXL_ID1,ADDR_MX_GOAL_POSITION1,dxl_goal_position):
    print(portHandler)
    print(DXL_ID1)
    print(ADDR_MX_GOAL_POSITION1)
    print(dxl_goal_position)
    DXL_MOVING_STATUS_THRESHOLD = 20 
    while 1: 
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID1, ADDR_MX_GOAL_POSITION, dxl_goal_position)
            print(f"t 12_po dx_{DXL_ID1} done!")
            while 1:
                print(f"t 3po dx_{DXL_ID1} open!")

                # Read present position
                dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID1, ADDR_MX_PRESENT_POSITION)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error))
                    
                if not abs(dxl_goal_position - dxl_present_position) < DXL_MOVING_STATUS_THRESHOLD:
                    
                    print(f"t 3po dx_{DXL_ID1} done!")
                    time.sleep(1)
                    return
                    
            
    return
def port_hand_ne(porthandler,DXL_ID1,ADDR_MX_GOAL_POSITION1,dxl_goal_position):
    print(portHandler)
    print(DXL_ID1)
    print(ADDR_MX_GOAL_POSITION1)
    print(dxl_goal_position)
    DXL_MOVING_STATUS_THRESHOLD = 20 
    while 1: 
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID1, ADDR_MX_GOAL_POSITION, dxl_goal_position)
            print(f"t 12_ne dx_{DXL_ID1} done!")
            while 1:
                print(f"t 3ne dx_{DXL_ID1} open!")

                dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID1, ADDR_MX_PRESENT_POSITION)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error))
                    
                if not abs(dxl_goal_position - dxl_present_position) < DXL_MOVING_STATUS_THRESHOLD:
                    
                    print(f"t 3ne dx_{DXL_ID1} done!")
                    time.sleep(1)
                    return
    return

def gripper(porthandler,DXL_ID1,ADDR_MX_GOAL_POSITION1,dxl_goal_position):
    print(portHandler)
    print(DXL_ID1)
    print(ADDR_MX_GOAL_POSITION1)
    print(dxl_goal_position)
    DXL_MOVING_STATUS_THRESHOLD = 20 
    while 1: 
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID1, ADDR_MX_GOAL_POSITION, dxl_goal_position)
            print(f"t gripper dx_{DXL_ID1} done!")
            while 1:
                print(f"t gripper dx_{DXL_ID1} open!")

                # Read present position
                dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID1, ADDR_MX_PRESENT_POSITION)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error))
                    
                if not abs(dxl_goal_position - dxl_present_position) < DXL_MOVING_STATUS_THRESHOLD:
                    
                    print(f"t gripper dx_{DXL_ID1} done!")
                    time.sleep(1)
                    return

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

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_MX_TORQUE_ENABLE      = 24               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36
ADDR_MOVING_SPEED          = 32

# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                      = 2                # Dynamixel ID : 1
BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 400           # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 620           # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

index = 0
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]         # Goal position


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()


# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 1, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 2, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 3, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 4, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, 5, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 1, ADDR_MOVING_SPEED, 50)
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 2, ADDR_MOVING_SPEED, 50)
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 3, ADDR_MOVING_SPEED, 50)
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 4, ADDR_MOVING_SPEED, 50)
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 5, ADDR_MOVING_SPEED, 50)
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 1, ADDR_MX_GOAL_POSITION, 700)
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 2, ADDR_MX_GOAL_POSITION, 2048)
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 3, ADDR_MX_GOAL_POSITION, 512)
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 4, ADDR_MX_GOAL_POSITION, 500)
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, 5, ADDR_MX_GOAL_POSITION, 500)

if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully connected")

while 1:    
    gripper(porthandler=portHandler,DXL_ID1=12,ADDR_MX_GOAL_POSITION1=ADDR_MX_GOAL_POSITION,dxl_goal_position=18500)
    time.sleep(1)
    port_hand_po(porthandler=portHandler,DXL_ID1=DXL_ID,ADDR_MX_GOAL_POSITION1=ADDR_MX_GOAL_POSITION,dxl_goal_position=dxl_goal_position[index])
    time.sleep(1)
    port_hand_ne(porthandler=portHandler,DXL_ID1=3,ADDR_MX_GOAL_POSITION1=ADDR_MX_GOAL_POSITION,dxl_goal_position=700)
    time.sleep(1)

    port_hand_po(porthandler=portHandler,DXL_ID1=1,ADDR_MX_GOAL_POSITION1=ADDR_MX_GOAL_POSITION,dxl_goal_position=500)
            
          
    gripper(porthandler=portHandler,DXL_ID1=12,ADDR_MX_GOAL_POSITION1=ADDR_MX_GOAL_POSITION,dxl_goal_position=25000)
    time.sleep(1)
    port_hand_ne(porthandler=portHandler,DXL_ID1=2,ADDR_MX_GOAL_POSITION1=ADDR_MX_GOAL_POSITION,dxl_goal_position=2048)
    time.sleep(1)
    port_hand_po(porthandler=portHandler,DXL_ID1=3,ADDR_MX_GOAL_POSITION1=ADDR_MX_GOAL_POSITION,dxl_goal_position=512)
        
    # Change goal position
    if index == 0:
        index = 1
    else:
        index = 0


# Disable Dynamixel Torque
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()