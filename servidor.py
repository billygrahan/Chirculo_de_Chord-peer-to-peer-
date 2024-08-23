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
                
                # Se a mensagem for uma lista de protocolo, exibir a lista
                try:
                    protocolo = eval(msg)  # Converte a string de volta para uma lista
                    if isinstance(protocolo, list) and len(protocolo) == 4:
                        print(f"{protocolo}")
                    elif str(msg).strip().lower() == "exit":
                        None
                    else:
                        print(f"Mensagem não reconhecida: {msg}")
                except:
                    print(f"Mensagem Recebida: {msg}")
                
                # Enviar resposta
                self.request.sendall(self.data)

            except Exception as e:
                print(f"Erro: {e}")
                print("*********************** CONNECTION DOWN ***********************")
                sys.exit()
            
            if str(msg).strip().lower() == "exit":
                print(f"Antecessor({Servidor.prompt}) saiu (e informou)!!!")
                sys.exit()


