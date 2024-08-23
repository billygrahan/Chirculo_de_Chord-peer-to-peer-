# .\.venv\Scripts\python.exe -m pip install readchar
#ss -ltn
import threading
import readchar
import sys
from time import sleep
from data_com import DataCom
from servidor import Servidor
from cliente import Cliente

if __name__ == "__main__":
    numero_de_pares = 2
    if len(sys.argv)>=2:
        numero_de_pares = int(sys.argv[1])

    info = DataCom("portas.txt", numero_de_pares)
    cliente = Cliente(info)
    servidor = Servidor(info, cliente)

    tserver = threading.Thread(target=servidor.run)#, args=(info,))
    tserver.start()
    sleep(1/10) 

    print(info) 
    print("****************** [<<ENTER>>=CONECTAR] ******************")
    
    enter = readchar.readkey()=='\n'
    if(enter):
        print("****************** [<<EXIT>>=SAIR] ******************")
        tclient = threading.Thread(target=cliente.run)#, args=(info,))
        tclient.start()
        tserver.join()
        tclient.join()
        print("********************************* FIM CONECTADO *********************************")
        print(repr(readchar.readkey()))
    else: 
        print("********************************* ABORT ANTES DE CONECTAR *********************************")
        cliente.close()
        print(repr(readchar.readkey()))
