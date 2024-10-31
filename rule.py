from enum import Enum

class Rule:
    def __init__(self, end_node, required_nodes):
        self.end_node = end_node
        self.required_nodes = required_nodes

        self.is_used = False
        
