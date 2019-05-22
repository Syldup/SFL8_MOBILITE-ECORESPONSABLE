#!/usr/bin/env python
#
# GrovePi Example for using the Grove GPS Module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html?cPath=25_130
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.
#                                                           
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      21 Aug 14 		Initial Authoring
# Karan		 10 June 15		Updated the code to reflect the decimal GPS coordinates (contributed by rschmidt on the DI forums: http://www.dexterindustries.com/forum/?topic=gps-example-questions/#post-5668)
import serial, time
import smbus
import math
import RPi.GPIO as GPIO
import struct
import sys

ser = serial.Serial(
   port='/dev/ttyAMA0',
   baudrate = 9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=0
)

ser.flush()

class GPS:
	#The GPS module used is a Grove GPS module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html
	inp=[]
	# Refer to SIM28 NMEA spec file http://www.seeedstudio.com/wiki/images/a/a0/SIM28_DATA_File.zip
	GGA=[]

	#Read data from the GPS
	def read(self):	
		while True:
			GPS.inp=ser.readline()
			if GPS.inp[:6] =='$GPGGA': # GGA data , packet 1, has all the data we need
				#print(1, GPS.inp)
				break
			time.sleep(0.1)     #without the cmd program will crach
		try:
			ind=GPS.inp.index('$GPGGA',5,len(GPS.inp))	#Sometimes multiple GPS data packets come into the stream. Take the data only after the last '$GPGGA' is seen
			
			GPS.inp=GPS.inp[ind:]
		except ValueError:
			pass
		GPS.GGA=GPS.inp.split(",")	#Split the stream into individual parts
		return [GPS.GGA]
		
	#Split the data into individual elements
	def vals(self):
		t=time.strftime('%H%M%S')
		lat=GPS.GGA[2]
		lat_ns=GPS.GGA[3]
		long=GPS.GGA[4]
		long_ew=GPS.GGA[5]
		fix=GPS.GGA[6]
		sats=GPS.GGA[7]
		alt=GPS.GGA[9]
		return [t,fix,sats,alt,lat,lat_ns,long,long_ew]
	
	# Convert to decimal degrees
	def decimal_degrees(self, raw_degrees):
		if raw_degrees == "":
			return 0
		degrees = float(raw_degrees) // 100
		d = float(raw_degrees) % 100 / 60
		return degrees + d

if __name__ == "__main__":	
	g=GPS()
	f=open("gps_data.csv",'w')	#Open file to log the data
	ind=0
	while True:
		try:
			x=g.read()	#Read from GPS
			[t,fix,sats,alt,lat,lat_ns,long,long_ew]=g.vals()	#Get the individial values
			
			# Convert to decimal degrees
			lat = g.decimal_degrees(lat)
			if lat_ns == "S":
				lat = -lat

			long = g.decimal_degrees(long)
			if long_ew == "W":
				long = -long
				
			print "Heure:",t,"Fix status:",fix,"Nb satellite:",sats,"Altitude",alt,"Lat:",lat,lat_ns,"Long:",long,long_ew
			s='"'+str(t)+'","'+str(float(lat))+'","'+str(float(long))+'"\n'
			f.write(s)	#Save to file
			time.sleep(2)
		except IndexError:
			print "Lecture impossible"
		except KeyboardInterrupt:
			f.close()
			print 'Sortir'
			sys.exit(0)
