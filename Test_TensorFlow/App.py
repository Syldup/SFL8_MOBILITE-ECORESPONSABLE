#!/usr/bin/env python3
import os
import __main__
import time
from Classe.camera import Camera
from Classe.interfaceBdd import InterfaceBdd

class App:
    def __init__(self):
        self.frequance_relever = 1

        self.main_path = os.path.dirname(__main__.__file__)

        self.inter = InterfaceBdd(7667, self.main_path+"/IMG")
        self.inter.syncroniser()

        self.capt = dict()
        self.capt["cam"] = Camera(self.main_path+"/IMG")
        self.capt["gps"] = None
        self.capt["MQ1365"] = None
        self.capt["particul"] = None

    def start(self):
        self.capt["cam"].open_win()
        for i in range(3):
            path = self.capt["cam"].get_value()
            print(path)
            time.sleep(self.frequance_relever)


if __name__=="__main__":

    app = App()
    app.start()
