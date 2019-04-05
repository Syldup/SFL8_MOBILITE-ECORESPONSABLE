#!/usr/bin/env python

from mySocket import MySocket, Serveur
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-a", "--address", default="10.16.37.181", help="address du serveur")
ap.add_argument("-p", "--port", type=int, default=7667, help="port de comunication")
ap.add_argument("-d", "--destination", default="./Import/", help="path to output images")
args = vars(ap.parse_args())

sock = MySocket(args["address"], args["port"])
sock.recv_dir(args["destination"])
sock.close()