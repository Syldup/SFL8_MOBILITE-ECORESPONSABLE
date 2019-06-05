#!/usr/bin/env python

import os
import __main__
import argparse
from Classe.mySocket import MySocket

main_path = os.path.dirname(__main__.__file__)

ap = argparse.ArgumentParser()
ap.add_argument("-a", "--address", default="10.16.37.183", help="address du serveur")
ap.add_argument("-p", "--port", type=int, default=7667, help="port de comunication")
ap.add_argument("-d", "--destination", default=main_path + "/Import/", help="path to output images")
args = vars(ap.parse_args())

sock = MySocket(args["address"], args["port"])
sock.recv_dir(args["destination"])
sock.close()