import random

from Graph import Vertex, Edge, Graph
from RandomGraph import RandomGraph

# Fifo based on Raymond Hettinger's recipe @http://code.active.state.com/recipes/68436
class Fifo(object):

    def __init__(self):
        self.nextin = 0
        self.nextout = 0
        self.data = {}

    def append(self, value):
        self.data[self.nextin] = value
        self.nextin += 1

    def pop(self, n=-1):
        value = self.data.pop(self.nextout)
        self.nextout += 1
        return value

    def is_empty(self):
        return self.nextout == self.nextin


class SmallWorldGraph(RandomGraph):

    def rewire(self, p):
        for v in self:
            for e in list(self.out_edges(v)):
                if random.random() < p:
                    new_edge = Edge(v, random.choice([w for w in self.vertices() if w is not v and self.get_edge(v,w) == None]))
                    self.add_edge(new_edge) #print 'Adding: %s\n' % ([new_edge])
                    self.remove_edge(e) #print 'Removing: %s' % [e]


    # The clustering coefficient measures whether vertices connected to a vertex v are also connected to each other,
    # i.e. the "clique-ishness" of a group of vertices.
    # See Watts & Strogatz paper for details on calculations.
    def clustering_coefficient(self):
        cc = 0.0
        for v in self.vertices():
            neighborhood_edges = []
            for w in self.out_vertices(v):
                for x in self.out_vertices(w):
                    e = Edge(w,x)
                    if x in self.out_vertices(v) and e not in neighborhood_edges and e not in self.out_edges(v):
                        neighborhood_edges.append(e)
            num_possible_edges = (len(self.out_vertices(v)) * (len(self.out_vertices(v))-1)) / 2.0
            if (num_possible_edges > 0):
                cc += len(neighborhood_edges) / num_possible_edges
        return cc / len(self.vertices())

    # The average path length measures the length of the shortest path between two vertices.
    # We are averaging the length of the shortest paths between all pairs of vertices.
    # This is calculated using Djikstra's shortest path algorithm.
    def average_path_length(self):       
        average = 0.0

        for v in self.vertices():
            path_lengths = {l:-1 for l in self.vertices()} #initialize path lengths to "infinite"
            queue = Fifo()
            queue.append(v)
            path_lengths[v] = 0

            while not queue.is_empty():
                current_node = queue.pop()
                for w in self.out_vertices(current_node):
                    if path_lengths[w] == -1:
                        queue.append(w)
                        path_lengths[w] = path_lengths[current_node] + 1

            average += sum(path_lengths.values()) / (len(self.vertices()))

        return average / len(self.vertices())
