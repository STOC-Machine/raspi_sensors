#! /usr/bin/env python

import io
import socket
import struct
import time
import picamera
from range_finder import range_finder
import RPi.GPIO as GPIO


# connect to server
client_socket = socket.socket()
client_socket.connect(('192.168.0.5', 8000))

# distance sensor socket
distance_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
distance_server = ('192.168.0.5', 8010)


# make file like object out of connection
connection = client_socket.makefile('wb')
# create range finder object
dist_sensor = range_finder()

try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        # start a preview and let camera warm up
        camera.start_preview()
        time.sleep(2)

        # make a stream to hold image data temporarly
        stream = io.BytesIO()
        for foo in camera.capture_continuous(stream, 'jpeg'):
            # write length and flush stream
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            # rewind stream and send image over wire
            stream.seek(0)
            connection.write(stream.read())
            #reset stream for next capture
            stream.seek(0)
            stream.truncate()
            
            # send distance data
            dist = dist_sensor.loop()
            distance_socket.sendto(str(dist), distance_server)

            #sleep
            #time.sleep(0.2)

    # write length zero to be done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
    distance_socket.close()
    GPIO.cleanup()
