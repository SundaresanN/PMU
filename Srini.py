####### MODULES #######
import sys
import gpsd
import time
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative
import socket

####### INITI #######

#gps = gpsd.connect(host='192.168.43.1',port= 2947)
#Only works with GPSD server format not with NMEA standard format
time.sleep(2)
print('connecting to Vehicle')
vehicle = connect('/dev/ttyS0',baud= 57600 ,wait_ready= True)

####### FUNCTIONS #######

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(2)


    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(2)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    # after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
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

###### MAIN #######

try:
    # Use the python gps package to access the laptop GPS
    gpsd.connect(host='192.168.43.1',port= 2947)
    time.sleep(2)
    print('Connected to Mobile GPS')
        #Arm and take off to an altitude of 5 meters
    arm_and_takeoff(5)

    while True:
            if vehicle.mode.name != "GUIDED":
                print "User has changed flight modes - aborting follow-me"
                break
            # Read the GPS state from the laptop
            try:
	    	packet = gpsd.get_current()
            	lat = packet.lat
            	lon = packet.lon

            # Once we have a valid location (see gpsd documentation) we can start moving our vehicle around
            	if lat !=0 and lon != 0:


		    altitude = 5  # in meters
                    dest = LocationGlobalRelative(packet.lat, packet.lon, packet.alt)
                    print "Going to: %s" % dest

                # A better implementation would only send new waypoints if the position had changed significantly
                    vehicle.simple_goto(dest)
                    time.sleep(2)
                # Send a new target every two seconds
                # For a complete implementation of follow me you'd want adjust this delay

	    except:
	        land()
                sys.exit(1)
except socket.error:
    print "Error: gpsd service does not seem to be running, plug in USB GPS or run run-fake-gps.sh"
    sys.exit(1)
