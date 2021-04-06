
import lib_car
import lib_pwm
import lib_i2c_handle
from lib_i2c_handle import I2C_Handle
from lib_gyro import *
from lib_VL53L0X import *
import servotester
from lib_car import myLenkServo
from lib_i2c_handle import I2C_Handle
from lib_pwm import PWM_Modul

def gyroServo(bus):
    gyro = Gyro_Modul(bus)


if __name__ == '__main__':
    try:
        bus = I2C_Handle()

        gyrotester(bus)
        distancetester(bus)

        bus.end()

    except KeyboardInterrupt:
        print("Shut down")

