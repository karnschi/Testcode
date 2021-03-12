#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Library fuer das Steuern des Fahrzeugs inkl. GPS Datenverarbeitung

Author: Thomas Karner
Date:   22.08.2017


"""
import time
import math
import RPi.GPIO as GPIO


MAX_LENKWINKEL      = 19.8
NOTAUS_PIN_BOARD    = 11

class CarControll:
    __count = 0
    def __init__(self, bus, Lenkservo, uno):
        print("\tInitialisiere Modell...")
        if CarControll.__count > 0:
            return
        CarControll.__count += 1
        self.bus = bus
        self.Lenkservo = Lenkservo
        self.Lenkwinkel = 0
        self.Speed = 0
        self.uno = uno
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(NOTAUS_PIN_BOARD, GPIO.OUT)
        print("\tModell initialisiert")
        return
    
    def ready2Drive(self):
        self.uno.getCarReady()
        GPIO.output(NOTAUS_PIN_BOARD, GPIO.HIGH)
        return
    
    def setSpeed(self, speed):
        self.Speed = speed
        self.uno.set_speed(speed)
        #time.sleep(0.1)
        return
    
    def setLenkwinkel(self, winkel):
        if winkel > MAX_LENKWINKEL:
            winkel = MAX_LENKWINKEL
        elif -winkel > MAX_LENKWINKEL:
            winkel = -MAX_LENKWINKEL
#        if winkel == 0:                            # Hier hätte die Funktion entstehen sollen die die Hysterese der Lenkung ausgleicht
#            if self.Lenkwinkel > 0:
#                self.Lenkservo.setLenkwinkel(-6)
#                time.sleep(0.05)
#            elif self.Lenkwinkel < 0:
#                self.Lenkservo.setLenkwinkel(6)
#                time.sleep(0.05)
        self.Lenkwinkel = winkel
        self.Lenkservo.setLenkwinkel(winkel)
        return
    
    def statusLenkwinkel(self):
        return self.Lenkwinkel
    
    def stop(self):
        GPIO.output(NOTAUS_PIN_BOARD, GPIO.LOW)
        self.Lenkservo.off()
        self.setSpeed(0)
        return
    
    def position(self):
        return self.uno.readgps()



class myLenkServo:
    __count = 0
    def __init__(self, pwmmodul, limit_min = 6, limit_max = 10.8, port = 0):
        if myLenkServo.__count > 0:
            return
        myLenkServo.__count += 1
        self.pwmmodul = pwmmodul
        self.port = port
        self.limit_min = limit_min
        self.limit_max = limit_max
        self.zero = (self.limit_max + self.limit_min)/2
        self.position = self.zero
        self.setServoPosition()
        return
    
    def setServoPosition(self, position):
        self.position = position
        self.pwmmodul.set_pwm(self.port, self.position)
        return
    
    def setLenkwinkel(self, lenkwinkel):
        self.position = (self.limit_max - self.limit_min) / (2 * MAX_LENKWINKEL)
        self.position *= (lenkwinkel + MAX_LENKWINKEL)
        self.position += self.limit_min
        self.setServoPosition()
        return
    
    def off(self):
        self.pwmmodul.set_pwm(self.port, 0)
        return
    
    def on(self):
        self.setServoPosition()
        return




if __name__ == '__main__':
    from lib_i2c_handle import I2C_Handle, I2C_Handle_Thread
    from lib_pwm import PWM_Modul
    from lib_uno import myUNO
    import time
    bus = I2C_Handle()
    i2c_thread = I2C_Handle_Thread(bus)
    i2c_thread.start()
    pwm = PWM_Modul(60, bus)
    uno = myUNO(bus)
    servo = myLenkServo(pwm)
    car = CarControll(bus, servo, uno)
    car.ready2Drive()
    
    try:
        while(1):
            winkel = input("Lenkwinkel: ")
            winkel = float(winkel)
            if math.fabs(winkel) < 19.1:
                car.setLenkwinkel(winkel)
                print(servo.position)
            elif winkel > 19.5:
                winkel -= 20
                winkel = int(winkel)
                car.setSpeed(winkel)
            else:
                print("Lenkwinkel nicht im vorgeschriebenen Bereich")
            
#            car.setLenkwinkel(19.5)
#            car.setSpeed(2)
#            print("Speed: 2")
#            time.sleep(10)
#            car.setLenkwinkel(0)
#            car.setSpeed(0)
#            print("Stop")
#            time.sleep(5)
            
            
#            car.setSpeed(3)
#            print("Speed: 3")
#            time.sleep(6)
#            car.setSpeed(0)
#            print("Speed: 0")
#            time.sleep(6)
#            car.setSpeed(2)
#            print("Speed: 2")
#            time.sleep(20)
            
#            car.setSpeed(5)
#            print("Speed: 5")
#            time.sleep(6)
#            car.setLenkwinkel(15)
#            print("Winkel: 15")
#            time.sleep(3)
#            car.setSpeed(7)
#            print("Speed: 7")
#            car.setLenkwinkel(0)
#            print("Winkel: 0")
#            time.sleep(3)
#            car.setSpeed(4)
#            print("Speed: 4")
#            time.sleep(3)
#            car.setLenkwinkel(-10)
#            print("Winkel: -10")
#            car.setSpeed(10)
#            print("Speed: 10")
#            time.sleep(4)
#            car.setLenkwinkel(0)
#            print("Winkel: 0")
#            time.sleep(3)
#            car.setSpeed(0)
#            print("Speed: 0")
#            time.sleep(15)
            
            
            
            
    except KeyboardInterrupt:
        car.stop();
        bus.end()
        i2c_thread.join()
        GPIO.cleanup();
        print("Ende")
        
        
        
        
        