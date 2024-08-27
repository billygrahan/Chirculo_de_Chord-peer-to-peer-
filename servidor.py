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

    def retorna_protocolo(self, protocolo):
        print(f"comando recebido: {protocolo}")  

        protocolo_resposta = protocolo
        protocolo_resposta[0] = protocolo[2]
        protocolo_resposta[3] = "assista my deer friend nokotan!!!"

        # Encaminha o protocolo para o próximo nó
        self.cliente.encaminhar_protocolo(protocolo_resposta)

    def handle(self):
        run, msg = True, ""
        while run:
            try:
                self.data = self.request.recv(1024).strip()
                msg = self.data.decode('utf-8')

                try:
                    protocolo = eval(msg)  # Converte a string de volta para uma lista

                    #verifica se está recebendo um protocolo!
                    if isinstance(protocolo, list) and len(protocolo) == 4:

                        # se o protocolo achar o nó correspondente reenvia a resposta!
                        if protocolo[0] == self.info.PORT_SERVER and protocolo[2] != self.info.PORT_SERVER:
                            self.retorna_protocolo(protocolo)

                        elif protocolo[2] == self.info.PORT_SERVER and protocolo[0] == protocolo[2]:
                            print(f"Recurso recebido: {protocolo[3]}")

                        #recebe a resposta do protocolo enviado
                        elif protocolo[2] == self.info.PORT_SERVER:
                            print(f"Recurso não encontrado: {protocolo}")

                        #reenvia o protocolo ao proximo nó
                        else:
                            # Encaminha o protocolo para o próximo nó
                            self.cliente.encaminhar_protocolo(protocolo)
                    

                    #recebe mensagem de sair do servidor anterior e não faz nada
                    elif str(msg).strip().lower() == "exit":
                        None
                    
                    #caso a mensagem não seja reconhecida!
                    else:
                        print(f"Mensagem não reconhecida: {msg}")
                
                #printa a mensagem em caso de mensagem recebida ser normal (ja implementado pelo professor)!
                except:
                    print(f"Mensagem Recebida: {msg}")

                # Enviar resposta ao remetente atual
                self.request.sendall(self.data)

            except Exception as e:
                print(f"Erro: {e}")
                print("*********************** CONNECTION DOWN ***********************")
                sys.exit()

            if str(msg).strip().lower() == "exit":
                print(f"Antecessor({self.info.host_name}) saiu (e informou)!!!")
                sys.exit()

            msg = None