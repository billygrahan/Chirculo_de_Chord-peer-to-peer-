import sys
import math

class DataCom:
    SHOST = "localhost" # Static: DataCom.SHOST
    SPORT = 3000        # Static: DataCom.SPORT
    FAIXA = 100
    M = 7  # Número de bits para o espaço de chaves

    def __init__(self, filename, numero_de_pares: int) -> None:
        if numero_de_pares <= 0:
            numero_de_pares = 1
        self.SIZE = numero_de_pares
        self.MAP = []
        for a in range(self.SIZE):
            server_port, client_port = a, (a + 1) % self.SIZE  # Ciclo circular
            self.MAP.append([server_port, client_port])
        self.IdxMap = self.__config_ports(filename)

    def __config_ports(self, filename):
        try:
            with open(filename, 'r') as f:
                _port = int(f.read())
            with open(filename, 'w') as f:
                f.write(str(_port + 1))
        except IOError:
            print("Erro ao ler arquivo!!")
            sys.exit()

        I = _port % self.SIZE
        self.HOST_SERVER = DataCom.SHOST
        self.PORT_SERVER = self.MAP[I][0] * DataCom.FAIXA + DataCom.SPORT
        self.SUCESSOR = self.MAP[I][1] * DataCom.FAIXA + DataCom.SPORT
        self.sucessor_name = f"NO[{self.SUCESSOR}]"
        self.host_name = f"NO[{self.PORT_SERVER}]"
        Ant_I = I - 1 if I - 1 >= 0 else self.SIZE - 1
        self.antecessor_name = f"NO[{self.MAP[Ant_I][0] * DataCom.FAIXA + DataCom.SPORT}]"

        self.node_id = self.PORT_SERVER % (2 ** self.M)  # Atribuir node_id dentro do espaço de chaves
        self.setF(I)

        return I

    def __repr__(self) -> str:
        s = "Servidor({0}), PortServer({1}), SUCESSOR({2} -> FAIXA[{3}-{4}]) ....".format(self.HOST_SERVER, str(self.PORT_SERVER), str(self.SUCESSOR), self.Fi, self.Fj) 
        return s + "\nCliente vais conectar assim: ESCUTA({0}), SUCESSOR({1}) OK!!".format(self.HOST_SERVER, str(self.SUCESSOR))

    def setF(self, I: int):
        self.Fi = int(self.SUCESSOR-DataCom.SPORT-DataCom.FAIXA + 1)
        self.Fj = int(self.SUCESSOR-DataCom.SPORT)
        if(I+1==self.SIZE): self.Fi = int(self.PORT_SERVER-DataCom.SPORT + 1) # Caso Faixa Final até zero

    def get_node_ids(self):
        return sorted([node_id % (2 ** self.M) for node_id in 
                      [self.MAP[i][0] * DataCom.FAIXA + DataCom.SPORT for i in range(self.SIZE)]])
    
    def fingerTable(self) -> list:
        finger_table = []
        node_ids = self.get_node_ids()
        node_id = self.node_id

        for j in range(self.M):
            start = (node_id + 2 ** j) % (2 ** self.M)
            successor = self.find_successor(start, node_ids)
            finger_table.append(successor)

        return finger_table

    def find_successor(self, start, node_ids):
        for nid in node_ids:
            if nid >= start:
                return nid
        return node_ids[0]
