import time
import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)

class Laser(object):

    def __init__(self):
        self.FREQ = 13 # Laser frequency (Hz)
        self.INPUT = 33
        self.setup()
        
    def setup(self):
        GPIO.setup(self.INPUT, GPIO.LOW)
        time.sleep(3) # Random waiting time. Can delete it.
    
    def blink(self):
        while True:
            self.activateLaser()
            time.sleep(1/self.FREQ)

    def activateLaser(self):
        GPIO.output(self.INPUT, True)
        time.sleep(0.001)
        GPIO.output(self.INPUT, False)

if __name__ == "__main__":
    laser = Laser()
    laser.blink()
    GPIO.cleanup()
