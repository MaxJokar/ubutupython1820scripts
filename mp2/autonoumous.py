# takeoff.py
from pymavlink import mavutil
import time


# mav_connection = mavutil.mavlink_connection('udpin:localhost:14550')

def arm_and_takeoff(aTargetAltitude):

    # wait for the first heart_beat
    # mav_connection.wait_heartbeat()
    print("heartbeat from the systesm(system %u  component %u )"% (mav_connection.target_system, mav_connection.target_component))
    #Output: heartbeat frm the systesm(system 1  component 0 )


    # Toget all messages :
    # while 1: 
    #     # msg = mav_connection.recv_match(blocking=True)
    #     msg = mav_connection.recv_match(type='ATTITUDE', blocking=True)
    #     print(msg)
    # ATTITUDE {time_boot_ms : 1009160, roll : -0.001169252092950046, pitch : -0.0011460429523140192, yaw : -0.33337557315826416, rollspeed : 0.0024112164974212646, pitchspeed : 0.0027868454344570637, yawspeed : 0.002661079866811633}


    """"
    2.How MAVLink command system work 
    MAVLink command (ARM command)to the vehicle

    """
    # ARM
    mav_connection.mav.command_long_send(mav_connection.target_system, mav_connection.target_component,
                                        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,0, 1, 0, 0, 0, 0, 0,0)

    msg = mav_connection.recv_match(type='COMMAND_ACK', blocking=True)
    print("ARM-DISARM:")
    print(msg)


    print("----------------------------------------")

    # takeoff
    mav_connection.mav.command_long_send(mav_connection.target_system, mav_connection.target_component,
                                        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,0, 0, 0, 0, 0, 0, 0,aTargetAltitude)

    # DISARM

    # mav_connection.mav.command_long_send(mav_connection.target_system, mav_connection.target_component,
    #                                      mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,0, 0, 0, 0, 0, 0, 0,0
    print("TAKE-OFF:")
    print("----------------------------------------")



    ans = str(input("if you want to land , choose y/n : "))
    if ans == "y":
        land()
    else:
        print("You did not choose Land mode  ")




    # msg = mav_connection.recv_match(blocking=True)
    print(msg)
    msg = mav_connection.recv_match(type='COMMAND_ACK', blocking=True)

def land():
        # Send a command to land
    mav_connection.mav.command_long_send(
        mav_connection.target_system, 
        mav_connection.target_component,
        mavutil.mavlink.MAV_CMD_NAV_LAND, 
        0, 0, 0, 0, 0, 0, 0, 0
    )
    print("Landing,............")

    # Wait for the acknowledgment
    ack = mav_connection.recv_match(type='COMMAND_ACK', blocking=True)
    if ack is None:
        print('No acknowledgment received within the timeout period.')
        return None

    return ack.result



def goto():
    mav_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, mav_connection.target_system,
                        mav_connection.target_component, mavutil.mavlink.MAV_FRAME_LOCAL_NED, int(0b100111111000), 40, 0, -10, 0, 0, 0, 0, 0, 0, 1.57, 0.5))

# while 1:
#     msg = mav_connection.recv_match(
#         type='MAV_CONTROLLER_OUTPUT', blocking=True)
#     print(msg)
    print("this is :MOVEMENT")
    while 1:
        msg = mav_connection.recv_match(
            type='LOCAL_POSITION_NED', blocking=True)
        print(msg)













if __name__ == '__main__':
    mav_connection = mavutil.mavlink_connection('udpin:localhost:14550')
    mav_connection.wait_heartbeat()

    h = float(input("please insert the height : "))
    arm_and_takeoff(h)
    time.sleep(25)
    print("Take off complete & hover for 20 sec")
    goto()

# Hover for 15 seconds
    print("Now  let's Land---")
    land()
    print("DONE")









