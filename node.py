class Node:
    def __init__(self, id, m):
        self.id = id
        self.m = m
        self.finger_table = []

    def calculate_finger_table(self, nodes):
        node_ids = sorted(node.id for node in nodes)
        for i in range(self.m):
            start = (self.id + 2**i) % 2**self.m
            successor = self.find_successor(start, node_ids)
            self.finger_table.append(successor)

    def find_successor(self, start, node_ids):
        for node_id in node_ids:
            if node_id >= start:
                return node_id
        return node_ids[0]

    def __str__(self):
        return f"Node({self.id}): {self.finger_table}"