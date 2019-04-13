import time
from .GPIOSetup import GPIO
from .setup import settings

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(11, GPIO.IN)

while True:
    i = GPIO.input(11)
    if i == 0:
        #print "No Human", i
        GPIO.output(17, 0)
        
    elif i == 1:
        GPIO.output(17, 1)


