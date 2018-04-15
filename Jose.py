from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative


vehicle = connect('/dev/ttyS0', wait_ready=True)


def takeoff(aTargetAltitude):
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    #while not vehicle.is_armable:
    #    print(" Waiting for vehicle to initialise...")
    #    time.sleep(1)

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

def land():
	vehicle.mode=VehicleMode("LAND")
	while True:
        	print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        	# Break and return from function just below target altitude.
        	if vehicle.location.global_relative_frame.alt < 1:
            		print("Reached ground")
            		break
        	time.sleep(1)

takeoff(2)
print('Hovering')
time.sleep(5)
#point1= LocationGlobalRelative(-35.3621542,149.1650704,10)
#vehicle.simple_goto(point1)
#time.sleep(30)
print('Landing Now')
land()

