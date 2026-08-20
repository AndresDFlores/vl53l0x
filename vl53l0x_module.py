"""
Wiring:

    VL53L0X Pin:Rasperry Pi Pico Pin

    VIN:3V3 (pin 36)
    GND:GND (pin 38)
    SCL:GP1 (pin 2)
    SDA:GP0 (pin 1)
"""

from machine import Pin, I2C
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

        #  telemetry log note
        print("Starting distance readings (Ctrl+C to stop)...")
