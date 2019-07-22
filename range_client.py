#! /usr/bin/env python 

from range_finder import range_finder
import socket
import time
import RPi.GPIO as GPIO

#set up connection
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.87', 8010))
print "connected"

#get range info
sensor = range_finder()

#send range
dist = sensor.loop()
s.send(str(dist))
#time.sleep(1)

GPIO.cleanup()
s.close()
