import os
from dynamixel_sdk import *


##################################################################
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

#################################################################

########## Register Initialization #############

ADDR_MX_TORQUE_ENABLE      = 24               
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36
ADDR_MOVING_SPEED          = 32

PROTOCOL_VERSION            = 1.0              
DXL_ID                      = 2                
BAUDRATE                    = 57600             
DEVICENAME                  = '/dev/ttyUSB0'    

TORQUE_ENABLE               = 1                 
TORQUE_DISABLE              = 0                 
DXL_MINIMUM_POSITION_VALUE  = 400          
DXL_MAXIMUM_POSITION_VALUE  = 620          
DXL_MOVING_STATUS_THRESHOLD = 20   


IDS = [1, 2, 3, 4, 5, 12]

GOALS = {
    1: 700,
    2: 2048,
    3: 512,
    4: 500, 
    5: 500
}

#################################################

index = 0
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]

##################################################

################# PORT HANDLER ###################

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




def torque_disable():
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    # Close port
    portHandler.closePort()

#####################################################

################## MOTOR FUNCTIONALITY ##############
def initialize_motor(dxl_id):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dxl_id, ADDR_MOVING_SPEED, 50)

    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print(f"Motor {dxl_id} has been successfully connected")


def move_motor(dxl_id, goal_position):
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, dxl_id, ADDR_MX_GOAL_POSITION, goal_position)

    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print(f"Motor {dxl_id} is moved to position {goal_position}")


def read_present_position(dxl_id):
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, dxl_id, ADDR_MX_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    return dxl_present_position

############################################################



################## INITIALIZATION ##########################
def initialize():
    for dxl_id in IDS:
        initialize_motor(dxl_id)
        move_motor(dxl_id, GOALS[dxl_id])

    print("INITIALIZATION SUCCESSFUL")

############################################################


def pick():
    move_motor(1, 500)
    move_motor(12, 18000)

    print("SUCCESS PICK")

def place():
    move_motor(3, 300)
    move_motor(12, 20000)

    print("SUCCESS PLACE")

def main():
    initialize()

    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(0x1b):
        torque_disable()
        return
    
    # start with motor 3
    move_motor(3, 700)
    while True:
        pres_pos_3 = read_present_position(3)
        if not abs(700 - pres_pos_3) > DXL_MOVING_STATUS_THRESHOLD:
            print("REACHED GOAL POSITION")
            torque_disable()
            return
        ######### IF COLOR DETECTION TRUE#######
        pick()
        time.sleep(1)

        place()
        time.sleep()

        GOALS[3] = pres_pos_3
        initialize()

        ########################################
    

