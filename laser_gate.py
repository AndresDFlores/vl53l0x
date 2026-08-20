import time
from vl53l0x_module import *


module_class = vl53l0xModule(scl_pin=1, sda_pin=0, freq=400000)
module_class.start_module()

iter_delay = 0.05

try:

    setpoint_data = []
    for _ in range(10):
        distance_mm = module_class.time_of_flight.read()
        setpoint_data.append(distance_mm)

    setpoint = sum(setpoint_data)/len(setpoint_data)


    while True:
        distance_mm = module_class.time_of_flight.read()

        if distance_mm<(setpoint*0.95):
            #  telemetry log note
            print(f'LASER TRIPPED: {distance_mm}mm')
            
        time.sleep(iter_delay)
    
except KeyboardInterrupt:
    module_class.time_of_flight.stop()
    print("Stopped.")