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
            
            if msg.strip().lower() == 'k':  # Se a mensagem for 'k'
                protocolo = []
                # Primeiro elemento: k porta a ser enviada a requisição
                protocolo.append(int(input("Digite a porta destino destino: ")))

                # Segundo elemento: String "localhost"
                protocolo.append("localhost")

                # Terceiro elemento: Porta do cliente que está enviando
                protocolo.append(self.info.PORT_SERVER)

                # Quarto elemento: String digitada pelo usuário
                protocolo.append(input("Digite a função: "))

                # Enviar a lista como string
                self.send(str(protocolo))

                self.receive()
            
            elif msg.strip().lower() != "":
                self.send(msg)
                self.receive()
                if str(msg).strip().lower() == 'exit':
                    self.close()
                    break


    def send(self, msg):
        if(self.connected):
            self.sc.sendall(msg.encode('utf-8'))

    def receive(self):
        if self.connected:
            try:
                rec_msg = self.sc.recv(1024).strip()
                rec_msg = rec_msg.decode('utf-8')
                
                # Verificar se a mensagem é uma lista de protocolo
                try:
                    protocolo = eval(rec_msg)
                    if isinstance(protocolo, list) and len(protocolo) == 4:
                        None
                    elif str(rec_msg).strip().lower() == "exit":
                        None
                    else:
                        print(f"Mensagem não reconhecida como protocolo: {rec_msg}")
                except:
                    #em caso de mensagens comuns sem protocolo
                    print(f"SUCESSOR({self.info.sucessor_name}):>> {rec_msg}")
            except ConnectionError as e:
                print(f"Erro de conexão: {e}")
            except Exception as e:
                print(f"Erro inesperado: {e}")

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

    def encaminhar_protocolo(self, protocolo):
        if protocolo[0] != self.info.PORT_SERVER:
            try:
                self.open()
                self.send(str(protocolo))
            except Exception as e:
                print(f"Erro ao encaminhar protocolo: {e}")

    
    """
    def resposta_protocolo(self, porta_destino, mensagem):
        # Cria um novo socket para enviar a resposta
        socket_resposta = socket.socket()

        try:
            socket_resposta.connect(("localhost",porta_destino))

            socket_resposta.sendall(mensagem.encode('utf-8'))

            print(f"Resposta enviada para {porta_destino}: {mensagem}")

            socket_resposta.close()
        except Exception as e:
            print(f"Erro ao enviar resposta para {porta_destino}: {e}")
            socket_resposta.close()"""