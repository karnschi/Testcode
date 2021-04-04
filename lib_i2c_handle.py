#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
I2C Handle fuer das SmartPiCar Projekt

Diese Bibliothek dient als Masterfunktion fuer den Zugriff auf den I2C Bus der
durch mehrere gleichzeitig laufende Threads zeitgleich erfolgen kann und somit
kontrolliert werden muss um Kollisionen vorzubeugen

Author: Thomas Karner
Date:   03.07.2017

"""

import smbus
import time
import multiprocessing

ID_MAX_COUNT = 100  # Gibt die maximale Anzahl der gleichzeitig reservierbaren IDs fuer Messages an

class I2C_Handle:
    __count = 0     # stellt sicher dass nur eine Instanz des I2C Handle gleichzeitig existieren kann
    
    def __init__(self):                 # Initialisierung
        if I2C_Handle.__count > 0:
            return
        
        print("\tInitialisiere I2C Handle...")
        
        self.online = True
        
        self.process_queue = multiprocessing.JoinableQueue()
        self.process_antwort = multiprocessing.Queue()
        self.process = multiprocessing.Process(target = self.data_transfer, args = (self.process_queue, self.process_antwort))
        self.process.start()
        
        I2C_Handle.__count += 1
        print("\tI2C initialisiert")                      # Initialisierung ist abgeschlossen
        return
        
#    def __del__(self):                                  # Selbstzerstoerungsmechanismus
#        #self.end()
#        I2C_Handle.__count -= 0
#        return
    
    def send_byte(self, add, reg, data="NO"):                        # Methode, die von anderen aufgerufen werden kann um ein Byte zu senden
        if data is not "NO":
            self.process_queue.put(("w", add, reg, data))
        else:
            self.process_queue.put(("w+", add, reg))
            # print("w+")
        self.process_queue.join()
        return
            
    def read_byte(self, add, reg="NO"):                              # Methode, die von anderen aufgerufen werden kann um ein Byte zu empfangen
        if reg is not "NO":
            self.process_queue.put(("r", add, reg))
        else:
            self.process_queue.put(("r+", add))
            # print("r+")
        self.process_queue.join()
        while True:
            data = self.process_antwort.get()
            return data
    
    def data_transfer(self, p, a):                                    # Methode die als Thread ablaufen kann um die Kommunikation auf dem i2c Bus zu organisieren
        process_queue = p
        process_antwort = a
        run = True
        bus = smbus.SMBus(1)
        while run:                                                # Moeglichkeit den Thread zu terminieren
            message = False
            message = process_queue.get()
#            self.process_queue.join()
            if message == "stop":
                process_queue.task_done()
                run = False
                return
            if message:
                message_type = message[0]
                if message_type == "w":
                    add = message[1]
                    reg = message[2]
                    data = message[3]
                    failed = 1000
                    while(failed > 0):
                        try:
                            bus.write_byte_data(add, reg, data)
                            failed = 0
                        except:
                            failed -= 1
                elif message_type == "w+":
                    add = message[1]
                    reg = message[2]
                    failed = 1000
                    while(failed > 0):
                        try:
                            bus.write_byte_data(add, reg)
                            failed = 0
                        except:
                            print("x")
                            failed -= 1
                elif message_type == "r":
                    add = message[1]
                    reg = message[2]
                    failed = 1000
                    while(failed > 0):
                        try:
                            data = bus.read_byte_data(add, reg)
                            failed = 0
                        except:
                            failed -= 1
                            data = 0x00
                    process_antwort.put(data)
                elif message_type == "r+":
                    add = message[1]
                    failed = 10
                    while (failed > 0):
                        try:
                            data = bus.read_byte_data(add)
                            failed = 0
                        except:
                            print("y")
                            failed -= 1
                            data = 0x00
                    process_antwort.put(data)
            process_queue.task_done()
        return

    def end(self):          # Beenden des Handlers
        self.online = False
        self.process_queue.put("stop")
        time.sleep(0.25)
        self.process.join()
        return

def I2C_Handle_Thread():
    return
    

            
    

