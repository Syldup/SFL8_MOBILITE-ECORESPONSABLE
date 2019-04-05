
import sys
sys.path.append('Library/')
from raspiomix import Raspiomix
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)            # mode de fonctionnement GPIO
GPIO.setup(Raspiomix.IO0, GPIO.IN) # configure port en sortie

r = Raspiomix()
ENTREE_CAN = 1
     
while True:
    print("La tension est de %f volt !" % r.readAdc(ENTREE_CAN))
    time.sleep(0)