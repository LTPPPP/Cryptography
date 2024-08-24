import hashlib
import time

class Node:
    def __init__(self, id, nodes):
        self.id = id
        self.nodes = nodes
        self.messages = []
        self.commit_count = 0
        self.pre_prepare = None
        self.prepare = None
        self.commit = None

    def broadcast(self, message):
        for node in self.nodes:
            if node.id != self.id:
                node.receive(message)

    def receive(self, message):
        self.messages.append(message)
        self.process_messages()

    def process_messages(self):
        for message in self.messages:
            if message['type'] == 'pre-prepare':
                self.handle_pre_prepare(message)
            elif message['type'] == 'prepare':
                self.handle_prepare(message)
            elif message['type'] == 'commit':
                self.handle_commit(message)
        self.messages = []

    def handle_pre_prepare(self, message):
        if self.pre_prepare is None:
            self.pre_prepare = message
            self.broadcast({'type': 'prepare', 'data': message['data']})

    def handle_prepare(self, message):
        if self.prepare is None:
            self.prepare = message
            self.broadcast({'type': 'commit', 'data': message['data']})

    def handle_commit(self, message):
        self.commit_count += 1
        if self.commit_count >= len(self.nodes) - 1:
            self.commit = message
            print(f"Node {self.id} committed: {message['data']}")

    def propose(self, data):
        self.pre_prepare = {'type': 'pre-prepare', 'data': data}
        self.broadcast(self.pre_prepare)

# Example usage
nodes = [Node(i, [Node(j, []) for j in range(4)]) for i in range(4)]

# Connect nodes
for node in nodes:
    node.nodes = nodes

# Propose a transaction
nodes[0].propose('Transaction data')

# Simulate message passing
for _ in range(3):
    for node in nodes:
        node.process_messages()
    time.sleep(1)
