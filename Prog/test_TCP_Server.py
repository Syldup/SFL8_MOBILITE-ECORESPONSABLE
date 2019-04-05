#!/usr/bin/env python

from mySocket import MySocket, Serveur
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port", type=int, default=7667, help="port de comunication")
ap.add_argument("-s", "--source", default="./images/", help="path to input images")
args = vars(ap.parse_args())

srv = Serveur(args["port"])
srv.set_source(args["source"])
srv.start()
srv.join()
