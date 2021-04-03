
import time
from lib_i2c_handle import I2C_Handle, I2C_Handle_Thread
import math
import numpy

# I2C Adresse
ADDRESS = 0x68  # Falls ein zweites Gyro Modul angeschlossen wird muss bei diesem der AD0 Pin auf VCC gelegt werden.
# Das zweite Modul kann dann ebenfalls mit den gleichen Befehlen automatisch instanziert werden, wobei es in der Reihenfolge als zweites angesprochen werden muss

# Register
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCELL_CONFIG = 0x1C
PWR_MGMT_1 = 0x6B
PWR_MGMT_2 = 0x6C

# Bits
CONFIG_SET = 0x00  # Setting fuer
GYRO_SET = 0x10  # Full Scale Range auf +-1000 Grad/s gesetzt
ACCELL_SET = 0x10  # Full Scale Range auf +-4g gesetzt
PWR_SET_1 = 0x00  # Power Management 1
PWR_SET_2 = 0x00  # Power Management 2

# Daten
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40

TEMP_OUT_H = 0x41
TEMP_OUT_L = 0x42

GYRO_XOUT_H = 0x43
GYRO_XOUT_L = 0x44
GYRO_YOUT_H = 0x45
GYRO_YOUT_L = 0x46
GYRO_ZOUT_H = 0x47
GYRO_ZOUT_L = 0x48


class Gyro_Modul:
    __count = 0  # Verhindert, dass mehr als eine Instanz erstellt wird

    def __init__(self, bus):  # Initialisierung
        if Gyro_Modul.__count > 1:
            print("Maximale Anzahl an Gyro Modulen wurden bereits initialisiert")
            return

        print("\tInitialisiere Gyro- und Beschleunigungs-Modul...")
        if Gyro_Modul.__count == 0:  # Zuweisung der Adresse am i2c Bus je nachdem wieviele Instanzen von diesem Modul bereits existieren
            self.address = ADDRESS
        else:
            self.address = ADDRESS + 1

        Gyro_Modul.__count += 1

        self.bus = bus

        self.bus.send_byte(self.address, CONFIG, CONFIG_SET)  # Senden der Konfiguration
        self.bus.send_byte(self.address, GYRO_CONFIG, GYRO_SET)
        self.bus.send_byte(self.address, ACCELL_CONFIG, ACCELL_SET)
        self.bus.send_byte(self.address, PWR_MGMT_1, PWR_SET_1)
        self.bus.send_byte(self.address, PWR_MGMT_2, PWR_SET_2)

        print("\tGyro- und Beschleunigungs-Modul initialisiert")  # Initialisierung abgeschlossen
        return

    def get_gyro_raw(self):  # Methode um die Rohdaten des Sensors abzurufen und in skalierbarer Art bereitzustellen
        x_msb = self.bus.read_byte(self.address, GYRO_XOUT_H)
        x_lsb = self.bus.read_byte(self.address, GYRO_XOUT_L)
        y_msb = self.bus.read_byte(self.address, GYRO_YOUT_H)
        y_lsb = self.bus.read_byte(self.address, GYRO_YOUT_L)
        z_msb = self.bus.read_byte(self.address, GYRO_ZOUT_H)
        z_lsb = self.bus.read_byte(self.address, GYRO_ZOUT_L)

        x = self._byte2word(x_msb, x_lsb)  # Umwandlung in 16Bit Zahl
        y = self._byte2word(y_msb, y_lsb)
        z = self._byte2word(z_msb, z_lsb)

        ro = self._komplement(x, 16)  # Roll
        pi = self._komplement(y, 16)  # Pitch
        ya = self._komplement(z, 16)  # Yaw

        return (ro, pi, ya)

    def get_gyro(
            self):  # Methode zum Abrufen der Winkelgeschwindigkeitswerte des Sensors und Rueckgabe in skalierter Form
        (roll, pitch, yaw) = self.get_gyro_raw()
        scale = 32.8
        roll = roll / scale
        pitch = pitch / scale
        yaw = yaw / scale
        return (roll, pitch, yaw)

    def get_acc_raw(self):  # Methode um die Rohdaten des Sensors abzurufen und in skalierbarer Art bereitzustellen
        x_msb = self.bus.read_byte(self.address, ACCEL_XOUT_H)
        x_lsb = self.bus.read_byte(self.address, ACCEL_XOUT_L)
        y_msb = self.bus.read_byte(self.address, ACCEL_YOUT_H)
        y_lsb = self.bus.read_byte(self.address, ACCEL_YOUT_L)
        z_msb = self.bus.read_byte(self.address, ACCEL_ZOUT_H)
        z_lsb = self.bus.read_byte(self.address, ACCEL_ZOUT_L)

        x = self._byte2word(x_msb, x_lsb)  # Umwandlung in 16Bit Zahl
        y = self._byte2word(y_msb, y_lsb)
        z = self._byte2word(z_msb, z_lsb)

        x = self._komplement(x, 16)
        y = self._komplement(y, 16)
        z = self._komplement(z, 16)
        return (x, y, z)

    def get_acc(self):  # Methode zum Abrufen der Beschleunigungswerte des Sensors und Rueckgabe in skalierter Form
        (x, y, z) = self.get_acc_raw()
        scale = 4096
        x = x / scale
        y = y / scale
        z = z / scale
        return (x, y, z)

    def get_temp(self):  # Methode zum Abrufen des Temperaturwerts des Sensors und Rueckgabe in skalierter Form
        t_msb = self.bus.read_byte(self.address, TEMP_OUT_H)
        t_lsb = self.bus.read_byte(self.address, TEMP_OUT_L)

        t = self._byte2word(t_msb, t_lsb)
        t = self._komplement(t, 16)
        t = t / 340.0 + 35
        return t

    def _komplement(self, val,
                    length):  # Methode wandelt einen Wert, der in 2er Komplementdarstellung eingegeben wird in einen Float Wert um
        if (val & (1 << length - 1)):
            val = val - (1 << length)
        return val

    def _byte2word(self, msb, lsb):  # Methode die dazu dient, aus zwei Byte einen 16Bit Wert zu erhalten
        val = msb << 8
        val += lsb
        return val

    def detectMovement(self, samples=10):
        movement = True

        ro_fifo = []
        pi_fifo = []
        ya_fifo = []

        for i in range(samples):
            (ro, pi, ya) = self.get_gyro()
            ro_fifo.append(ro)
            pi_fifo.append(pi)
            ya_fifo.append(ya)
            # time.sleep(0.05)

        while (movement):
            ro_mean = numpy.mean(ro_fifo)
            pi_mean = numpy.mean(pi_fifo)
            ya_mean = numpy.mean(ya_fifo)

            (ro, pi, ya) = self.get_gyro()

            ro_diff = ro_mean - ro
            pi_diff = pi_mean - pi
            ya_diff = ya_mean - ya
            #            print("%4.2f,   \t %4.2f,   \t %4.2f,   \t %4.2f,   \t %4.2f,   \t %4.2f,   \t %4.2f,   \t %4.2f,   \t %4.2f" % (ro, pi, ya, ro_mean, pi_mean, ya_mean, ro_diff, pi_diff, ya_diff))

            ro_limit = 0.5  # 0.25
            pi_limit = 0.5  # 0.25
            ya_limit = 1  # 0.75

            if math.fabs(ro_diff) < ro_limit and math.fabs(pi_diff) < pi_limit and math.fabs(ya_diff) < ya_limit:
                movement = False
                break;
            else:
                ro_fifo.append(ro)
                pi_fifo.append(pi)
                ya_fifo.append(ya)
                ro_fifo.remove(ro_fifo[0])
                pi_fifo.remove(pi_fifo[0])
                ya_fifo.remove(ya_fifo[0])
                # time.sleep(0.05)
        return

def gyrotester(bus):
    gyro = Gyro_Modul(bus)
    for i in range(100):
        (x, y, z) = gyro.get_acc()
        (ro, pi, ya) = gyro.get_gyro()
        g = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        (x, y, z) = (x/g, y/g, z/g)
        g = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        t = gyro.get_temp()
        print("Acc: %4.2f,   \t %4.2f,   \t %4.2f,   \t %4.2f \t Gyro: %4.2f,   \t %4.2f,   \t %4.2f \t Temp: %4.2f" % (
        x, y, z, g, ro, pi, ya, t))
        time.sleep(0.25)

