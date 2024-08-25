import threading
import readchar
import sys
import math
from time import sleep
from data_com import DataCom
from servidor import Servidor
from cliente import Cliente
from node import Node

def fingerTable():
    try:
        node_ids = [0, 1, 3, 4, 6]
        m = math.ceil(math.log2(len(node_ids)))
        nodes = [Node(id, m) for id in node_ids]

        for node in nodes:
            node.calculate_finger_table(nodes)

        for node in nodes:
            print(node)
    except Exception as e:
        print("Erro: ", str(e))

def main():
    numero_de_pares = 2
    if len(sys.argv) >= 2:
        try:
            numero_de_pares = int(sys.argv[1])
        except ValueError:
            print("Número de pares inválido, utilizando 2 por padrão.")
            numero_de_pares = 2

    try:
        info = DataCom("portas.txt", numero_de_pares)
        
        cliente = Cliente(info)
        servidor = Servidor(info, cliente)

        tserver = threading.Thread(target=servidor.run)
        tserver.start()
        sleep(0.1)

        print(info)
        print("****************** [<<ENTER>>=CONECTAR] ******************")

        enter = readchar.readkey() == '\r'
        if enter:
            print("****************** [<<EXIT>>=SAIR] ******************")
            fingerTable()
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
