import threading
import readchar
import sys
import math
from time import sleep
from data_com import DataCom
from servidor import Servidor
from cliente import Cliente
from node import Node

def main():
    # Defina o número total de nós na rede
    total_nodes = 4  # Por exemplo, 4 nós
    if len(sys.argv) >= 2:
        try:
            total_nodes = int(sys.argv[1])
        except ValueError:
            print("Número de pares inválido, utilizando 4 por padrão.")
            total_nodes = 4

    try:
        info = DataCom("portas.txt", total_nodes)
        
        cliente = Cliente(info)
        servidor = Servidor(info, cliente)

        finger_table = info.fingerTable()
        print("Finger Table: ")
        for id, finger in enumerate(finger_table, start=1):
            print(f"ID{id}: {finger}")

        tserver = threading.Thread(target=servidor.run)
        tserver.start()
        sleep(0.1)

        print(info)
        print("****************** [<<ENTER>>=CONECTAR] ******************")

        enter = readchar.readkey() == '\r'
        if enter:
            print("****************** [<<EXIT>>=SAIR] ******************")
            tclient = threading.Thread(target=cliente.run)
            tclient.start()
            tserver.join()
            tclient.join()
            print("********************************* FIM CONECTADO *********************************")
            print(repr(readchar.readkey()))
        else:
            print("********************************* ABORT ANTES DE CONECTAR *********************************")
            cliente.close()
            print(repr(readchar.readkey()))
    except Exception as e:
        print("Erro: ", str(e))
        print(repr(readchar.readkey()))
    finally:
        try:
            cliente.close()
        except Exception as e:
            print("Erro ao fechar o cliente: ", str(e))

if __name__ == "__main__":
    main()
