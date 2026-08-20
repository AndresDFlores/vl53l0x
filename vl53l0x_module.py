"""
Wiring:

    VL53L0X Pin:Rasperry Pi Pico Pin

    VIN:3V3 (pin 36)
    GND:GND (pin 38)
    SCL:GP1 (pin 2)
    SDA:GP0 (pin 1)
"""

from machine import Pin, I2C
import time
from vl53l0x_driver import VL53L0X  # https://github.com/uceeatz/VL53L0X


class vl53l0xModule:

    def check_module(self, i2c):
        devices = i2c.scan()
        if not devices:
            raise RuntimeError("No I2C devices found. Check wiring.")
        print("I2C devices found:", [hex(d) for d in devices]) 

    def __init__(self, scl_pin:int, sda_pin:int, freq:int):

        i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)
        self.check_module(i2c)  # optional

        self.time_of_flight = VL53L0X(i2c)  

    def start_module(self):
        self.time_of_flight.start()
        print("Starting distance readings (Ctrl+C to stop)...")


if __name__=='__main__':
    module_class = vl53l0xModule(scl_pin=1, sda_pin=0, freq=400000)
    module_class.start_module()

    iter_delay = 0.05

    try:
        while True:
            distance_mm = module_class.time_of_flight.read()
            print("Distance: {} mm".format(distance_mm))
            time.sleep(iter_delay)
    except KeyboardInterrupt:
        module_class.time_of_flight.stop()
        print("Stopped.")