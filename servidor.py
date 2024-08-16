import socketserver
import sys

class Servidor:
    prompt = "HOST"
    def __init__(self, _info):
        self.info = _info
        Servidor.prompt = self.info.host_name
    def run(self): 
        with socketserver.TCPServer((self.info.HOST_SERVER, self.info.PORT_SERVER), ComunicadorTCPHandler) as server: 
            try: 
                server.serve_forever()
            finally: server.shutdown() #except KeyboardInterrupt: #pass # server.server_close()

############################################## Classe de Apoio ao Server ###########################################
class ComunicadorTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        run, msg = True, ""
        while run:
            try:
                self.data = self.request.recv(1024).strip()
                msg = self.data.decode('utf-8')
                print("PEER: {0}, Mensagem: {1}\n{2}:>> ".format(self.client_address[0], msg, Servidor.prompt), end="")
                #print("Client:>> ", end="")
                self.request.sendall(self.data.upper())

            except:
                print("*********************** CONNECTION DOWN ***********************")
                sys.exit()
            if str(msg).strip().lower() == "exit":
                print("Antecessor({0}) saiu (e informou)!!!".format(Servidor.prompt))
                sys.exit()

