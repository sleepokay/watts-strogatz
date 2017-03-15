class Vertex(object):
    def __init__(self, label=''):
        self.label = label

    def __repr__(self):
        return 'Vertex(%s)' % repr(self.label)

    __str__ = __repr__


class Edge(tuple):
    def __new__(cls, *vs):
        if len(vs) != 2:
            raise ValueError, 'Edges must connect exactly two vertices.'
        return tuple.__new__(cls, vs)

    def __repr__(self):
        return 'Edge(%s, %s)' % (repr(self[0]), repr(self[1]))

    __str__ = __repr__


class Graph(dict):
    def __init__(self, vs=[], es=[]):
        for v in vs:
            self.add_vertex(v)
            
        for e in es:
            self.add_edge(e)

    def add_vertex(self, v):
        self[v] = {}

    def add_edge(self, e):
        v, w = e
        self[v][w] = e
        self[w][v] = e

    def get_edge(self, v1, v2):
        try:
            return self[v1][v2]
        except KeyError:
            return None

    def remove_edge(self, e):
        if self.get_edge(e[0], e[1]) != None:
            del self[e[0]][e[1]]
            del self[e[1]][e[0]]
            del e

    def vertices(self):
        return self.keys()

    def edges(self):
        edges = []
        for v in self:
            for w in self[v]:
                if self[v][w] != {} and self[v][w] not in edges:
                    edges.append(self[v][w])
        return edges

    def out_vertices(self, v):
        return self[v].keys()

    def out_edges(self, v):
        edges = []
        for w in self[v]:
            if self[v][w] != {} and self[v][w] not in edges:
                edges.append(self[v][w])
        return edges

    def add_all_edges(self):
        for v in self:
            for w in self:
                if v != w:
                    self.add_edge(Edge(v,w))

    def add_regular_edges(self, k):
        """the necessary and sufficient condition for a k-regular graph of order n to exist
        are that n>=k+1 and that n*k is even"""
        if (len(self.vertices()) <= k or (len(self.vertices())*k) % 2 != 0):
            print 'preconditions not met'
            return

        vs = self.vertices()

        for i in range(len(vs)):
            for j in range(i - (k/2), i + (k/2)-1):
                if (i != j):
                        self.add_edge(Edge(vs[i], vs[j % len(vs)]))

                if (k%2 != 0):
                    self.add_edge(Edge(vs[i], vs[ (i+(len(vs)/2)) % len(vs)]))

    def is_connected(self):
        start = self.vertices()[0]
        queue = []
        marked = []
        queue.append(start)

        while (queue):
            current = queue[0]
            marked.append(current)
            queue.remove(queue[0])

            for w in self.out_vertices(current):
                if w not in marked and w not in queue:
                    queue.append(w)

        if set(marked) == set(self.vertices()):
            print 'Connected!'
            return True
        else:
            print 'Not connected!'
            return False


def main(script, *args):
    v = Vertex('v')
    w = Vertex('w')
    x = Vertex('x')
    e = Edge(v, w)
    d = Edge(v, x)
    
    g = Graph([v,w,x], [e,d])
    print g
    print

    print g.vertices()

    print g.edges()

    print g.out_vertices(v)

    print g.out_edges(v)

    g.add_all_edges()

    print g

if __name__ == '__main__':
    import sys
    main(*sys.argv)