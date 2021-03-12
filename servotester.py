import threading
import time

from lib_car import myLenkServo
from lib_i2c_handle import I2C_Handle
from lib_pwm import PWM_Modul

angle = 0
minAngle = float(7)
maxAngle = float(9)

def twistingThread(servo):#, minAngle, maxAngle):
    try:
        global angle
        global minAngle
        global maxAngle
        position = 3
        print(str(minAngle) + "  " + str(maxAngle))
        while(angle < 1000):
            minA = minAngle
            maxA = maxAngle

            steps = 60
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
    servo1 = myLenkServo(pwm, port = 0)

    twister1 = threading.Thread(target=twistingThread, args=[servo1])#, 3, 15])
    twister1.start()


    global angle
    global minAngle
    global maxAngle
    try:
        while(True):
            minAngle = float(input(str(minAngle) + " und neues Minimum: "))
            maxAngle = float(input(str(maxAngle) + " und neues Maximum: "))

            if minAngle > 100 or maxAngle > 100:
                break

            if minAngle < 1.0:
                minAngle = 1.0
            if maxAngle > 16.0:
                maxAngle = 16.0
        angle = 1000
        bus.end()

    except KeyboardInterrupt:
        print("EPIC FAIL")
        angle = 1000
        bus.end()

