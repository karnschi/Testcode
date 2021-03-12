import threading
import time

from lib_car import myLenkServo
from lib_i2c_handle import I2C_Handle
from lib_pwm import PWM_Modul

angle = 0
minAngle = 0
maxAngle = 0

def twistingThread(servo, minAngle, maxAngle):
    try:
        position = 0
        while(angle < 1000):
            minA = minAngle
            maxA = maxAngle
            steps = 30
            timestep = 1 / steps
            step = (maxA - minA) / steps

            while(position < maxA):
                servo.setServoPosition(position)
                time.sleep(timestep)
                position += step

            while (position > minA):
                servo.setServoPosition(position)
                time.sleep(timestep)
                position -= step
        servo.setServoPosition(0)
        return
    except KeyboardInterrupt:
        print("something failed")
    return


def testRun():
    bus = I2C_Handle()
    pwm = PWM_Modul(60, bus)
    servo = myLenkServo(pwm)

    twister = threading.Thread(target=twistingThread, args=[servo, 3, 15])
    twister.start()

    try:
        while(True):
            minAngle = input("Minimum: ")
            maxAngle = input("Maximum: ")

            if minAngle > 100 or maxAngle > 100:
                break

            if minAngle < 3:
                minAngle = 3
            if maxAngle > 15:
                maxAngle = 15
        angle = 1000
        bus.end()

    except:
        angle = 1000
        bus.end()

