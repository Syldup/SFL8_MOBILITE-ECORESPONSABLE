#!/usr/bin/env python
import os
import time
import pathlib
from mySocket import MySocket

source = pathlib.Path(os.getcwd() + '/Image/none')

sock = MySocket()
sock.bind("localhost", 6666)
sock.accept()

for path in list(source.glob('*')):

    sock.sendFile(path)
    data = sock.receive()
    if data != "ok":
        break;

sock.close()