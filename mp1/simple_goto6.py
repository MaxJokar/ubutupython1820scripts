from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative

# Set up option parsing to get connection string
import argparse



parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
# parser.add_argument('--connect',
#                     help="Vehicle connection target string. If not specified, SITL automatically started and used.")
parser.add_argument('--connect', default='127.0.0.1:14550')
args = parser.parse_args()
connection_string = args.connect
sitl = None


# Start SITL if no connection string specified
# if not connection_string:
#     import dronekit_sitl
#     sitl = dronekit_sitl.start_default()
#     connection_string = sitl.connection_string()


# Connect to the Vehicle
print('----Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)
# aTargetAltitude = float(input("Please input the relevant hight: " ))

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    def decorator(func):

        def wrapper(*args, **kwargs):
            print("----Basic pre-arm checks")
        # Don't try to arm until autopilot is ready
            while not vehicle.is_armable:
                print("----Waiting for vehicle to initialise...")
                time.sleep(1)

            print("----Arming motors")
            # Copter should arm in GUIDED mode
            vehicle.mode = VehicleMode("GUIDED")
            
            vehicle.armed = True

            # Confirm vehicle armed before attempting to take off
            while not vehicle.armed:
                print("----Waiting for arming...")
                time.sleep(1)

            print("----Taking off!")

            vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

            # Wait until the vehicle reaches a safe height before processing the goto
            #  (otherwise the command after Vehicle.simple_takeoff will execute
            #   immediately).
            while True:
                print("----Altitude: ", vehicle.location.global_relative_frame.alt)
                # Break and return from function just below target altitude.
                if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
                    break
                time.sleep(1)
            print("------------END UAV Climbing...----------------------------------\n")
            # print(f"----Reached target altitude: {aTargetAltitude}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# print("-----------------------------------------")
# Get user input
# h = int(input("Please input the relevant hight: " ))
# arm_and_takeoff(h)


@arm_and_takeoff(aTargetAltitude= float(input("Please input the relevant hight: " )))

def goto():
    # print("----Set default/target airspeed to  You  favorite Hight ")
    # s = float(input("Please input the relevant Speed : " ))
    lat = float(input("----Please give 1 value for  Latitude, Exmple -35.3609336  :"))
    lon = float(input("----Please give 1 value the Longitude,Example  149.1648209  :"))
    # alt = input("----Please give 1 value the Altitude Up to 100 : ")

    print("")
    print("-----Going towards given waypoints  for 20 seconds ...")
    point1 = LocationGlobalRelative(lat, lon)
    # point1 = LocationGlobalRelative(lat, lon, alt)
    print("all is OK  so far.......")
    # vehicle.simple_goto(point1, groundspeed=float(s))

    # sleep so we can see the change in map
    time.sleep(30)


def change_uav_mode():
    
    # uavmode = str(input("please change the uav  mode RTL, GUIDED, STB:"))
    # time.sleep(10)
    # if uavmode == "GUIDED" :
    #     vehicle.mode = VehicleMode("GUIDED" )
    #     # time.sleep(5) 
    # elif uavmode == "STB":
    #     vehicle.mode = VehicleMode("STABILIZE")
    #     # time.sleep(5)    
    # else:
    #     print("nohting")
    #     vehicle.mode = VehicleMode("RTL")
    # time.sleep(10)


    # uavmode = raw_input("Please change the UAV mode (RTL, GUIDED, STABILIZE): ").strip().upper()
    uavmode = str(input("Please change the UAV mode (RTL, GUIDED, STABILIZE): ").strip().upper())

    valid_modes = ["RTL", "GUIDED", "STABILIZE"]

    if uavmode in valid_modes:
        print ("Changing mode to %s" , uavmode)
        vehicle.mode = VehicleMode(uavmode)
    else:
        print ("Invalid mode. Please enter RTL, GUIDED, or STABILIZE.")


  
    vehicle.close() 
    if sitl:
        sitl.stop()



# def RTL():
#     print("----Returning to Launch")
#     vehicle.mode = VehicleMode("RTL")

#     # Close vehicle object before exiting script
#     print("----Close vehicle object")
#     vehicle.close()

#     # Shut down simulator if it was started.
#     if sitl:
#         sitl.stop()









# def RTL():
#     print("----Returning to Launch")
#     vehicle.mode = VehicleMode("RTL")

#     # Close vehicle object before exiting script
#     print("----Close vehicle object")
#     vehicle.close()

#     # Shut down simulator if it was started.
#     if sitl:
#         sitl.stop()



# if __name__ == "__main__":
#     h = int(input("Please input the relevant hight: " ))
#     arm_and_takeoff(h)
#     print("-------------PART goto  point-------------------")
#     goto()
#     print("-------------RTL-------------------")
#     RTL()


if __name__ == "__main__":
    # aTargetAltitude = float(input("Please input the relevant hight: " ))
    goto()
    # arm_and_takeoff(h)
    # print("-------------PART goto  point-------------------")
    # print("-------------RTL-------------------")
    change_uav_mode()
    # RTL()

