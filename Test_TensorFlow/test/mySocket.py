import socket
import time

class MySocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.client_socket = None
        self.addr = ""

    def connect(self, host, port):
        self.sock.connect((host, port))

    def bind(self, host, port):
        self.sock.bind((host, port))
        self.sock.listen(1)

    def accept(self):
        self.client_socket, self.addr = self.sock.accept()
        print("Connect to - ", self.addr)

    def close(self):
        if self.client_socket is not None:
            self.client_socket.close()
        self.sock.close()

    def send(self, msg):
        totalsent = 0
        msg = str.encode(msg)
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent += sent

    def sendFile(self, file_name):
        if self.client_socket is not None:
            f = open(file_name, 'rb')
            self.client_socket.sendfile(f, 0)
            f.close()
            print(".", end='')

    def receive(self):
        chunks = []
        while len(chunks) == 0 or chunk:
            chunk = self.sock.recv(2048)
            if chunk:
                chunks.append(chunk)
            else:
                time.sleep(5)
        print(end='.')
        return b''.join(chunks)
