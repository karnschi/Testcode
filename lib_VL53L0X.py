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
        GPIO.setup(self.GPIO1_Pin, GPIO.OUT)
        GPIO.setup(self.XSHUT_Pin, GPIO.IN)
        xshut_on()

        print(self.bus.read_byte(self.address, 0xC0))
        print(self.bus.read_byte(self.address, 0xC1))
        print(self.bus.read_byte(self.address, 0xC2))
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
