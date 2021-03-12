import servotester
import lib_car
import lib_pwm
import lib_i2c_handle


if __name__ == '__main__':
    try:
        servotester.testRun()
    except:
        print("Shut down")

