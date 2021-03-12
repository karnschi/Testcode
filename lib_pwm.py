#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Library fuer das PWM Modul

Bibliothek zum Ansteuern des PWM Moduls mit dem PCA9685 Chipsatz

Author: Thomas Karner
Date:   03.07.2017


"""

import time
from lib_i2c_handle import *
import math

# I2C Adresse
ADDRESS = 0x40

# Register
MODE1       = 0x00
MODE2       = 0x01
PRESCALE    = 0xFE

# Channel
CH0_ON_LSB  = 0x06
CH0_ON_MSB  = 0x07
CH0_OFF_LSB  = 0x08
CH0_OFF_MSB  = 0x09


# Bits
SLEEP       = 0x10
RESET       = 0x80
ALLCALL     = 0x01
OUTDRV      = 0x04


class PWM_Modul:
    __count = 0     # Verhindert, dass mehr als eine Instanz erstellt wird
    def __init__(self, freq, bus):
        if PWM_Modul.__count > 0:
            return
        
        print("\tInitialisiere PWM Modul...")
        PWM_Modul.__count += 1
        self.address = ADDRESS
        self.bus = bus
        
        self.bus.send_byte(self.address, MODE2, OUTDRV)
        self.bus.send_byte(self.address, MODE1, ALLCALL)
        time.sleep(0.005)
        
        self.set_freq(freq) # Setzen der gewuenschten Frequenz
        for i in range(0,16):   # Alle PWM Ausgaenge werden bei der Initialisierung auf Null geschaltet
            self.set_pwm(i, 0)
            self.set_pwm_on(i, 0)
        
        
        print("\tPWM Modul initialisiert")    # Initialisierung abgeschlossen
        return

    def set_freq(self, freq):   # Methode zum Aendern der Grundfrequenz nach Ablauf der im Datenblatt beschriebenen Schritte
        oldmode = self.bus.read_byte(self.address, MODE1)
        newmode = (oldmode & 0x7F) | 0x10
        resetmode = oldmode | 0x80
        
        self.bus.send_byte(self.address, MODE1, newmode)        # Sleepmode
        time.sleep(0.005)
        
        prescale = math.floor(25e6/(4096 * freq) - 0.5)         # Prescale berechnen
        prescale = 0x79
        
        self.bus.send_byte(self.address, PRESCALE, prescale)    # Prescale einstellen
        time.sleep(0.005)
        
        self.bus.send_byte(self.address, MODE1, oldmode)        # Sleepmode beenden
        time.sleep(0.005)
        
        self.bus.send_byte(self.address, MODE1, resetmode)      # Reset - hierdurch wird der neue Prescale Wert wirksam
        time.sleep(0.005)
        self.freq = freq
        
        return
    
    def set_pwm(self, channel, dutycycle):    # Dutycycle muss in Prozent (0-100) angegeben werden
        dc = math.floor(dutycycle * 4096 / 100 + 0.5)   # Umrechnung des Dutycycle von Prozent in einen geeigneten Bitwert mit 12Bit Basis
        ch_lsb = CH0_OFF_LSB + 4 * channel    # Erstellung der einzelnen Bytes die in die Register geschrieben werden muessen
        ch_msb = CH0_OFF_MSB + 4 * channel
        
        dc_lsb = dc & 0xFF
        dc_msb = dc >> 8
        
        self.bus.send_byte(self.address, ch_lsb, dc_lsb)    # Schreiben der Daten
        self.bus.send_byte(self.address, ch_msb, dc_msb)
        return
    
    def set_pwm_on(self, channel, dutycycle):    # Dutycycle muss in Prozent (0-100) angegeben werden
        dc = math.floor(dutycycle * 4096 / 100 + 0.5)   # Umrechnung des Dutycycle von Prozent in einen geeigneten Bitwert mit 12Bit Basis
        ch_lsb = CH0_ON_LSB + 4 * channel        # Erstellung der eizelnen Byte die in die Register geschrieben werden muessen
        ch_msb = CH0_ON_MSB + 4 * channel
        
        dc_lsb = dc & 0xFF
        dc_msb = dc >> 8
        
        self.bus.send_byte(self.address, ch_lsb, dc_lsb)    # Schreiben der Daten
        self.bus.send_byte(self.address, ch_msb, dc_msb)
        return
        
        
if __name__ == '__main__':
    
    mode = 2
    
    from lib_i2c_handle import I2C_Handle, I2C_Handle_Thread
    bus = I2C_Handle()
    i2c_thread = I2C_Handle_Thread(bus)
    i2c_thread.start()
    pwm = PWM_Modul(60, bus)
    minn = 400
    maxx = 1500
    pre = 100
    c0_0 = range(minn,maxx, 1)
    c0_1 = range(-maxx, -minn, 1)
    print("\nTestmodus\n")

    try:
        if mode == 1:
            while(True):
                for i in c0_0:
                    pwm.set_pwm(0, i/pre)
                    pwm.set_pwm(1, i/pre)
                    pwm.set_pwm(2, (i/pre)-1)
                    time.sleep(0.04)
                    for i in c0_1:
                        pwm.set_pwm(0, -i/pre)
                        pwm.set_pwm(1, -i/pre)
                        pwm.set_pwm(2, (-i/pre)+1)
                        time.sleep(0.04)
        elif mode == 2:
            while (True):
                steps = 4#471
                minn = 6#3.5
                maxx = 10.8#13
                x1 = range(0,steps)
                x2 = range(-steps,0)
                step = (maxx - minn) / steps
                
                for i in x1:
                    pwm.set_pwm(0, i * step + minn)
                    print(i * step + minn)
                    time.sleep(1.5)
                for i in x2:
                    pwm.set_pwm(0, -i * step + minn)
                    print(-i * step + minn)
                    time.sleep(1.5)
        else:
#            for i in range(0,16):   # Alle PWM Ausgaenge werden bei der Initialisierung auf Null geschaltet
#                pwm.set_pwm(i, 50)
#            print("done")
            while(True):
                time.sleep(1)
                
    except KeyboardInterrupt:
        for i in range(0,16):
            pwm.set_pwm(i, 0)
        bus.end()
        i2c_thread.join()
        print("Ende")






















        