
import lib_car
import lib_pwm
import lib_i2c_handle
from lib_i2c_handle import I2C_Handle
from lib_gyro import *
import servotester

if __name__ == '__main__':
    try:
        bus = I2C_Handle()
        #servotester.testRun(bus)

        gyrotester(bus)

        bus.end()

    except KeyboardInterrupt:
        print("Shut down")

