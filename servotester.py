import threading
import time

from lib_car import myLenkServo
from lib_i2c_handle import I2C_Handle
from lib_pwm import PWM_Modul

angle = 0
minAngle = float(2)
maxAngle = float(5)

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

            steps = 30
            timestep = 1.5 / steps
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
    except:
        print("something failed")
    return


def testRun():
    bus = I2C_Handle()
    pwm = PWM_Modul(60, bus)
    servo = myLenkServo(pwm)

    twister = threading.Thread(target=twistingThread, args=[servo])#, 3, 15])
    twister.start()

    global angle
    global minAngle
    global maxAngle
    try:
        while(True):
            minAngle = float(input(str(minAngle) + " und neues Minimum: "))
            maxAngle = float(input(str(maxAngle) + " und neues Maximum: "))

            if minAngle > 100 or maxAngle > 100:
                break

            if minAngle < 3:
                minAngle = 3
            if maxAngle > 15:
                maxAngle = 15
        angle = 1000
        bus.end()

    except KeyboardInterrupt:
        print("EPIC FAIL")
        angle = 1000
        bus.end()

