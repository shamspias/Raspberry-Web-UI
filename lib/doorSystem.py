import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(5, GPIO.OUT)

p = GPIO.PWM(5, 50)

p.start(7.5)


def doorClose():
    p.ChangeDutyCycle(7.5) # turn towards 180 degree
    time.sleep(10) # sleep 1 second

def doorOpen():
    p.ChangeDutyCycle(2.5)  # turn towards 90 degree
    time.sleep(1) # sleep 1 second