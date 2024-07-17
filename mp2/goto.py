# takeoff.py
# MP must be in GUIDED mode  !!!!
import argparse
from pymavlink import mavutil

#mav_connection = mavutil.mavlink_connection('udpin:localhost:14552')
#mav_connection = mavutil.mavlink_connection('udpin:localhost:14550')
mav_connection = mavutil.mavlink_connection('127.0.0.1:14552')

# wait for the first heart_beat
mav_connection.wait_heartbeat()
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
print("this is :MAV_CMD_COMPONENT_ARM_DISARM")
print(msg)


# take-off
mav_connection.mav.command_long_send(mav_connection.target_system, mav_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,0, 1, 0, 0, 0, 0, 0,10)
msg = mav_connection.recv_match(type='COMMAND_ACK', blocking=True)
print("this is :MAV_CMD_NAV_TAKEOFF")
print(msg)



# DISARM
# mav_connection.mav.command_long_send(mav_connection.target_system, mav_connection.target_component,
#                                      mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,0, 0, 0, 0, 0, 0, 0,0)
# msg = mav_connection.recv_match(blocking=True)
# msg = mav_connection.recv_match(type='COMMAND_ACK', blocking=True)
# print("this is :MAV_CMD_NAV_TAKEOFF")
# print(msg)




# goto:SET_POSTION_TARGET_LOCAL_NED==> SET THE VEHICLES TARGET POSITION
# SET_POSTION_TARGET_LOCAL_NED(10,TS,TC,COORDINATE_FRAME,TYPE_MASK,X,Y,Z,VX,VY,VZ,YAW, YAW_RATE) 
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







# mav_connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_global_int_message(10, mav_connection.target_system,
#                         mav_connection.target_component, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, int(0b110111111000), int(-35.3629849 * 10 ** 7), int(149.1649185 * 10 ** 7), 10, 0, 0, 0, 0, 0, 0, 1.57, 0.5))



# LAND
# mav_connection.mav.command_long_send(mav_connection.target_system, mav_connection.target_component,
#                                      mavutil.mavlink.MAV_CMD_NAV_LAND_LOCAL,0, 0, 0, 0, 0, 0, 0,0)
# msg = mav_connection.recv_match(type='COMMAND_ACK', blocking=True)
# print("this is :MAV_CMD_NAV_LAND_LOCAL")
# print(msg)


# while 1:
#     msg = mav_connection.recv_match(
#         type='LOCAL_POSITION_NED', blocking=True)
#     print(msg)







