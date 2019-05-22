from gps import GPS
import time

g=GPS()

try:
	print("Valeur obtenue : {}".format(g.decimal_degrees("00133.5752")))
except ValueError as err:
	print(err)

time.sleep(10)
