
import lib_car
import lib_pwm
import lib_i2c_handle
from lib_i2c_handle import I2C_Handle
from lib_gyro import *
import servotester
from lib_car import myLenkServo
from lib_i2c_handle import I2C_Handle
from lib_pwm import PWM_Modul

def gyroServo(bus):
    gyro = Gyro_Modul(bus)


if __name__ == '__main__':
    try:
        bus = I2C_Handle()
        print(bus.read_byte(0x70, 0x75))
        print(bus.read_byte(0x75))
        bus.send_byte(0x75, 0x01, 0x01)
        print(bus.read_byte(0x75))
        for i in range(112,120):
            print(bus.read_byte(0x75))
        #servotester.testRun(bus)

        gyrotester(bus)

        bus.end()

    except KeyboardInterrupt:
        print("Shut down")

