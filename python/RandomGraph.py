import random
from Graph import Graph, Vertex, Edge

class RandomGraph(Graph):

    def add_random_edges(self, p):
        for v in self:
            for w in self:
                if v != w and random.random() < p:
                    self.add_edge(Edge(v,w))