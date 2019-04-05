#!/usr/bin/env python

import socket
import struct
import pathlib
from threading import Thread 


class MySocket:
    def __init__(self, addr=None, port=None, sock_src=None):
        if sock_src is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((addr, port))
        else:
            self.sock = sock_src

    def send_dir(self, directory="."):
        directory = pathlib.Path(directory)

        for path in list(directory.glob('*')):
            print(path.name)
            if path.is_dir():
                self.send_msg(b"/"+path.name.encode()+b"/")
                self.send_dir(path)
            elif path.is_file():
                self.send_msg(path.name.encode())
                self.send_file(path)

        self.send_msg(b"Fini")

    def recv_dir(self, directory="."):
        directory = pathlib.Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        
        msg = self.recv_msg().decode("utf-8")
        while msg != 'Fini':
            if msg[-1] == "/":
                self.recv_dir(directory.as_posix()+msg)
            else:
                print(directory.as_posix()+"/"+msg)
                data = self.recv_msg()
                f = open(directory.as_posix()+"/"+msg, 'wb')
                f.write(data)
                f.close()

            msg = self.recv_msg().decode("utf-8")

    def close(self):
        self.sock.close()

    def send_msg(self, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        self.sock.sendall(msg)

    def send_file(self, file_name):
        f = open(file_name, 'rb')
        self.send_msg(f.read())
        f.close()

    def recv_msg(self):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(msglen)

    def recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data


class Serveur(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("", port))
        self.server.listen(2)
        self.source = "."
        print("Start ...")
    
    def run(self):
        while True:
            sock, addr = self.server.accept()
            print("Connect to - ", addr)

            sock = MySocket(sock_src=sock)
            sock.send_dir(self.source)
            sock.close()
            print("Deconnect")

    def set_source(self, src):
        self.source = src
