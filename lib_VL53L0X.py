import time
import math
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

ADDRESS_TOF = 0x29
PIN_ON = GPIO.HIGH
PIN_OFF = GPIO.LOW
PIN_OUT = GPIO.OUT
PIN_IN = GPIO.IN


class VL53L0X:
    def __init__(self, bus, GPIO1_Pin, XSHUT_Pin):
        self.GPIO1_Pin = GPIO1_Pin
        self.XSHUT_Pin = XSHUT_Pin
        self.bus = bus
        self.address = ADDRESS_TOF
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO1_Pin, GPIO.IN)
        GPIO.setup(self.XSHUT_Pin, GPIO.OUT)
        time.sleep(0.01)
        self.xshut_on()

        print(self.bus.read_byte(self.address, 0xC0) == 0xEE)
        print(self.bus.read_byte(self.address, 0xC1) == 0xAA)
        print(self.bus.read_byte(self.address, 0xC2) == 0x10)

        print(hex(self.bus.read_byte(self.address, 0xC0)))

        nn = 0
        ff = 0
        ol = 0
        for i in range(256):
            ans = self.bus.read_byte(self.address, i)
            if ans is not 0 and ans is not 0xFF:
        #        print(str(i) + ". - " + hex(i) + " :: " + hex(ans))
                if ans < 0x10:
                    ol += 1
            else:
                nn += 1
            if ans is 0xFF:
                ff += 1

        print(str(nn) + " 0x00")
        print(str(ff) + " 0xFF")
        print(str(ol) + " < 0x0F")

        return

    def xshut_on(self):
        GPIO.output(self.XSHUT_Pin, GPIO.HIGH)
        time.sleep(0.005)
        return

    def xshut_off(self):
        GPIO.output(self.XSHUT_Pin, GPIO.LOW)
        return

    def readGPIO(self):
        return GPIO.input(self.GPIO1_Pin)


def distancetester(bus):
    tofsensor1 = VL53L0X(bus, 12, 16)
