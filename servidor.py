import socketserver
import sys

class Servidor:
    def __init__(self, _info, _cliente):
        self.info = _info
        self.cliente = _cliente

    def run(self):
        with socketserver.TCPServer((self.info.HOST_SERVER, self.info.PORT_SERVER), self.handler_factory) as server:
            try:
                server.serve_forever()
            finally:
                server.shutdown()

    def handler_factory(self, *args, **kwargs):
        return ComunicadorTCPHandler(self.info, self.cliente, *args, **kwargs)

class ComunicadorTCPHandler(socketserver.BaseRequestHandler):
    def __init__(self, info, cliente, *args, **kwargs):
        self.info = info
        self.cliente = cliente
        super().__init__(*args, **kwargs)

    def handle(self):
        run, msg = True, ""
        while run:
            try:
                self.data = self.request.recv(1024).strip()
                msg = self.data.decode('utf-8')

                try:
                    protocolo = eval(msg)
                    if isinstance(protocolo, list) and len(protocolo) == 4:
                        if protocolo[0] == self.info.PORT_SERVER:
                            print(f"comando recebido:{protocolo}")
                            self.cliente.resposta_cliente_protocolo(protocolo[2], protocolo[3])
                        else:
                            # Encaminha o protocolo para o próximo nó
                            self.cliente.encaminhar_protocolo(protocolo)
                    elif str(msg).strip().lower() == "exit":
                        None
                    else:
                        print(f"Mensagem não reconhecida: {msg}")
                except:
                    print(f"Mensagem Recebida: {msg}")
                
                # Enviar resposta ao nó anterior em caso de mensagens comuns
                self.request.sendall(self.data)

            except Exception as e:
                print(f"Erro: {e}")
                print("*********************** CONNECTION DOWN ***********************")
                sys.exit()
            
            if str(msg).strip().lower() == "exit":
                print(f"Antecessor({self.info.host_name}) saiu (e informou)!!!")
                sys.exit()
