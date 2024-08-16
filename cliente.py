import socket

class Cliente:
    def __init__(self, _info):
        self.sc = socket.socket()
        self.info = _info
        self.connected = False
        self.prompt = self.info.host_name + ":>> "
    
    def run(self):
        self.open()
        while True:
            msg = input(str(self.prompt))
            if(msg.strip()!=""):
                self.send(msg)
                self.receive()
                if(str(msg).strip().lower()=='exit'): 
                    self.close()
                    break

    def send(self, msg):
        if(self.connected): 
            self.sc.sendall(msg.encode('utf-8'))

    def receive(self):
        if(self.connected): 
            rec_msg = self.sc.recv(1024).strip()
            rec_msg = rec_msg.decode('utf-8')
            print("SUCESSOR({0}):>> {1}".format(self.info.sucessor_name, rec_msg))

    def close(self):
        self.open()
        self.send("exit")
        self.receive()

    def open(self):
        if(self.connected==False):
            try: 
                self.sc.connect((self.info.HOST_SERVER, self.info.SUCESSOR))
                self.connected = True
            except IOError: 
                print("SUCESSOR({0}), Host({1}), PORTA({2}) Falhou!!".format(self.info.sucessor_name, self.info.HOST_SERVER, str(self.info.SUCESSOR)))
                self.connected = False
