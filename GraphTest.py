import string
import numpy

from Graph import Vertex, Edge, Graph
from SmallWorldGraph import SmallWorldGraph

def main(script, n='1000', k='10', *args):

    n = int(n) #number of vertices
    k = int(k) #number of edges in regular graph
    vertices = [Vertex(c) for c in range(n)]

    g = SmallWorldGraph(vertices)
    g.add_regular_edges(k)

    #regular graph's clustering coefficient and avg path length
    c_zero = g.clustering_coefficient()
    l_zero = g.average_path_length()
    print c_zero, l_zero

    f = open("plots/output.csv", "wb")
    print 'p\tC\tL'
    f.write('p,C(p)/C(0),L(p)/L(0)\n')

    #begin rewiring to tease out small-world network characteristics
    for log_exp in numpy.arange(-40, 1, 1): #incrementation scheme for logarithmic exponents
        g = SmallWorldGraph(vertices)
        g.add_regular_edges(k)
        p = numpy.power(10, log_exp/10.0)
        g.rewire(p)
        print '%s\t%s\t%s' % (p, g.clustering_coefficient()/c_zero, g.average_path_length()/l_zero)
        f.write('%s,%s,%s\n' % (p, g.clustering_coefficient()/c_zero, g.average_path_length()/l_zero))
    f.close()


if __name__ == '__main__':
    import sys
    main(*sys.argv)