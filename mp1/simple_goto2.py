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
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


arm_and_takeoff(30)

print("Set default/target airspeed to 30")
vehicle.airspeed = 30

print("Going towards first point :North- for 30 seconds ...")
# point1 = LocationGlobalRelative(-35.361354, 149.165218, 50)
point1 = LocationGlobalRelative(-35.3609336, 149.1648209, 50) # North
vehicle.simple_goto(point1)

# sleep so we can see the change in map
time.sleep(30)

print("Going towards second point for 10 seconds :South East- (groundspeed set to 50 m/s) ...")
#point2 = LocationGlobalRelative(-35.363244, 149.168801, 30)
point2 = LocationGlobalRelative(-35.3629723, 149.1616344, 30) # South East
vehicle.simple_goto(point2, groundspeed=50)

# sleep so we can see the change in map
time.sleep(50)



print("Going towards third point:South for 20 seconds (groundspeed set to 20 m/s) ...")
#point3 = LocationGlobalRelative(-35.363244, 149.168801, 30)
point3 = LocationGlobalRelative( -35.3639347,149.1653788 , 30) # South
vehicle.simple_goto(point3, groundspeed=20)

# sleep so we can see the change in map
time.sleep(50)





print("Going towards fourth point for 20 seconds (groundspeed set to 50 m/s) ...")
#point4 = LocationGlobalRelative(-35.363244, 149.168801, 20)
point4 = LocationGlobalRelative( -35.3642059,149.1653466 , 20) # South
vehicle.simple_goto(point4, groundspeed=5)

# sleep so we can see the change in map
time.sleep(50)

# WANT TO TEST IF GUIDE CAN BE CHANGED TO AUTO MODE OR  NOT !!!!!TEST
#print("wait for the next command for 20 sec Otherwise RTL")
#vehicle.mode = VehicleMode("AUTO")
#time.sleep(50)



# Copter should arm in GUIDED mode
#vehicle.mode = VehicleMode("GUIDED")
#time.sleep(10)






print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl:
    sitl.stop()



