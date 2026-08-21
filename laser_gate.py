import time
from collections import deque
from vl53l0x_module import *


class LaserGate:

    #  use VL53L0X to log when objects pass through the chute slide

    def __init__(self):

        #  start vl53l0x module
        self.module_class = vl53l0xModule(scl_pin=1, sda_pin=0, freq=400000)
        self.module_class.start_module()

        #  class variables
        self.iter_delay = 0.05  # how long between each data read
        self.gate_flag = deque([False, False],2)  # track gate crossing


    def monitor_gate(self):

        try:

            #  establish a gate beam length setpoint as an average measurement, tof
            setpoint_data = []
            for _ in range(10):
                distance_mm = self.module_class.time_of_flight.read()
                setpoint_data.append(distance_mm)

            setpoint = sum(setpoint_data)/len(setpoint_data)
            #  log setpoint value and time measured


            #  continually monitor gate for bean interruptions
            while True:
                distance_mm = self.module_class.time_of_flight.read()


                #  beam interruption if measured distance is less than 95% of setpoint
                if distance_mm<(setpoint*0.95):
                    #  telemetry log note
                    self.gate_flag.append(True)
                else:
                    self.gate_flag.append(False)


                #  compare current iter flag to previous iter flag to determine interruption status
                flag_sum = self.gate_flag[-1]-self.gate_flag[0]
                if flag_sum==1:
                    print(f'Object Crossed Laser Gate')
                    #  log gate cross event time 


                #  wait until executing next loop
                time.sleep(self.iter_delay)

            
        except KeyboardInterrupt:
            self.module_class.time_of_flight.stop()
            print("Stopped.")


if __name__=="__main__":
    LaserGate().monitor_gate()
