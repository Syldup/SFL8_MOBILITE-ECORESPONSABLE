#!/usr/bin/env python
import os
import time
import pathlib
from mySocket import MySocket

destination = str(os.getcwd()) + '/Import/'

sock = MySocket()
sock.connect("localhost", 6666)

nbimg = 0

while True:
    data = sock.receive()
    f = open(destination+'img_'+ str(nbimg)+".jpg", 'wb')
    f.write(data)
    f.close()
    nbimg += 1

    sock.send("ok")