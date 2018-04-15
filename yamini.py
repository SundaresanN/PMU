import forecastio as wdata
from dronekit import connect, VehicleMode, Command, LocationGlobalRelative

api_key = "a775d03803ae94f391562eb1c9cda333"

print('connecting to Vehicle')
vehicle = connect('/dev/ttyS0', baud = 57600 ,wait_ready= True)

while 1:
    lat = vehicle.location._lat
    lon = vehicle.location._lon
    if lat!=0 and lon!=0:
        data = wdata.load_forecast (api_key , lat , lon)
        current_data = data.currently()
        data = dict(current_data.d)
        for i in(data):
            print (i ,' :', data[i])
        break