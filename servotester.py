import threading
import time

from lib_car import myLenkServo
#from lib_i2c_handle import I2C_Handle
from lib_pwm import PWM_Modul

angle = 0
minAngle = float(6.3)
maxAngle = float(10)
turning = False

def twistingThread(servo):#, minAngle, maxAngle):
    try:
        global angle
        global minAngle
        global maxAngle
        global turning
        position = minAngle
        print(str(minAngle) + "  " + str(maxAngle))
        while(angle < 1000 and turning):
            minA = minAngle
            maxA = maxAngle

            steps = 1
            turningtime = 4
            timestep = turningtime / steps
            step = (maxA - minA) / steps

            servo.setServoPosition(minAngle)
            for i in range(steps):
                time.sleep(timestep)
                position = position + step
                servo.setServoPosition(position)

            for i in range(steps):
                time.sleep(timestep)
                position = position - step
                servo.setServoPosition(position)


        servo.setServoPosition(0)
        return
    except KeyboardInterrupt:
        print("something failed")
    return


def testRun(bus=I2C_Handle()):
    pwm = PWM_Modul(60, bus)
    servo = myLenkServo(pwm, port = 0)

    #twister1 = threading.Thread(target=twistingThread, args=[servo1])#, 3, 15])
    #twister1.start()


    global angle
    global minAngle
    global maxAngle
    global turning
    turning = False
    t = False
    manual = True
    position = 8
    try:
        while(True):
            while(manual):
                position = float(input("Neuer Wert: "))
                if position == 123:
                    turning = True
                    t = True
                    manual = False
                if position > 500:
                    manual = False
                    break
                servo.setServoPosition(position)

            while(turning):
                if t:
                    twister1 = threading.Thread(target=twistingThread, args=[servo])  # , 3, 15])
                    twister1.start()
                    t = False

                minAngle = float(input(str(minAngle) + " und neues Minimum: "))
                maxAngle = float(input(str(maxAngle) + " und neues Maximum: "))

                if minAngle == 123 or maxAngle == 123:
                    manual = True
                    turning = False

                if minAngle > 500 or maxAngle > 500:
                    turning = False
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

