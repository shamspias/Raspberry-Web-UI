#Sensors are not fully implemented yet it's now testing condition

import RPi.GPIO as GPIO

def pirS():
    while True:
        if GPIO.input(23):
            return 1
        else:
            return 0