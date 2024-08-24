# .\.venv\Scripts\python.exe -m pip install readchar
#ss -ltn
import threading
import readchar
import sys
from time import sleep
import math
from data_com import DataCom
from servidor import Servidor
from cliente import Cliente

class Node:
    def __init__(self, identifier, m):
        self.identifier = identifier
        self.m = m
        self.finger_table = []

    def calculate_finger_table(self, nodes):
        for i in range(1, self.m + 1):
            start = (self.identifier + 2**(i-1)) % 2**self.m
            successor = self.find_successor(start, nodes)
            self.finger_table.append(successor)

    def find_successor(self, id, nodes):
        for node in nodes:
            if node.identifier >= id:
                return node.identifier
        return nodes[0].identifier

    def __repr__(self):
        return f"Node({self.identifier}): {self.finger_table}"

def main():
    numero_de_pares = 2
    if len(sys.argv) >= 2:
        try:
            numero_de_pares = int(sys.argv[1])
        except ValueError:
            print("Numero de pares invalido, utilizando 2 por padrao.")
            numero_de_pares = 2

    try:
        info = DataCom("portas.txt", numero_de_pares)
        cliente = Cliente(info)
        servidor = Servidor(info, cliente)

        tserver = threading.Thread(target=servidor.run)#, args=(info,))
        tserver.start()
        sleep(1/10) 

        print(info) 
        print("****************** [<<ENTER>>=CONECTAR] ******************")
        
        enter = readchar.readkey()=='\r'
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
    except Exception as e:
        print("Erro: ", str(e))
        print(repr(readchar.readkey()))
    finally:
        try:
            cliente.close()
        except Exception as e:
            print("Erro ao fechar o cliente: ", str(e))
        
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


if __name__ == "__main__":
    main()