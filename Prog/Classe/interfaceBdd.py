#!/usr/bin/env python3
import socket
from threading import Thread
from Classe.mySocket import MySocket, Serveur

class InterfaceBdd:
    def __init__(self, port, source):
        self.port = port
        self.source = source

    def is_connected(self):
        try: # Test la connection a un hote
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            pass
        return False

    def syncroniser(self):
        if not self.is_connected():
            return

        def func():
            self.start_srv_trandfer(self.source, mode="send-rm")

        Thread(target=func).start()

    def start_srv_trandfer(self, source, mode="send-rm"):
        srv = Serveur(self.port, source)
        srv.set_mode(mode)
        srv.start()

    def recv_img(self, ip, source="."):
        sock = MySocket(ip, self.port)
        sock.recv_dir(source)
        sock.close()
