#!/usr/bin/env python3


import time
import serial
import RPi.GPIO as GPIO

ser = serial.Serial(
   port='/dev/ttyAMA0',
   baudrate = 9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=5
)
ser.flush()
counter = 50

while counter > 0:
   x=ser.readline()
   print(x)
   counter -= 1



