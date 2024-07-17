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
            print("------------END UAV Climbing...----------------------------------")
            # print(f"----Reached target altitude: {aTargetAltitude}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# print("-----------------------------------------")
# Get user input
# h = int(input("Please input the relevant hight: " ))
# arm_and_takeoff(h)


@arm_and_takeoff(30)
def goto():
    print("----Set default/target airspeed to  You  favorite Hight ")
    s = input("Please input the relevant Speed : " )
    vehicle.airspeed = s
    lat = input("----Please give 1 value for  Latitude, Exmple :-35.3609336\n ")
    lon = input("----Please give 1 value the Longitude,Example  149.1648209\n ")
    alt = input("----Please give 1 value the Altitude Up to 100 : \n")
    print("")
    print("-----Going towards given waypoints  for 50 seconds ...")
    # point1 = LocationGlobalRelative(-35.361354, 149.165218, 50)
    # point1 = LocationGlobalRelative(-35.3609336, 149.1648209, 50) # North
    point1 = LocationGlobalRelative(lat, lon, alt)
    vehicle.simple_goto(point1)

    # sleep so we can see the change in map
    time.sleep(50)


def RTL():
    print("----Returning to Launch")
    vehicle.mode = VehicleMode("RTL")

    # Close vehicle object before exiting script
    print("----Close vehicle object")
    vehicle.close()

    # Shut down simulator if it was started.
    if sitl:
        sitl.stop()



# if __name__ == "__main__":
#     h = int(input("Please input the relevant hight: " ))
#     arm_and_takeoff(h)
#     print("-------------PART goto  point-------------------")
#     goto()
#     print("-------------RTL-------------------")
#     RTL()


if __name__ == "__main__":
    aTargetAltitude = float(input("Please input the relevant hight: " ))
    goto()
    # arm_and_takeoff(h)
    print("-------------PART goto  point-------------------")
    print("-------------RTL-------------------")
    RTL()

