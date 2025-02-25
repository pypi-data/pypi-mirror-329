from .UnionFind import UnionFind
from .PriorityQueue import PQ


class Node:
    def __init__(self, key, value=None):
        self._edges_out = {}
        self.edges_in = set()

        self.key = key
        self.value = value

    def addEdge(self, point_to: 'Node', weight=None):
        self._edges_out[point_to] = weight
        point_to.edges_in.add(self)

    def breakEdge(self, point_to: 'Node'):
        self._edges_out.pop(point_to)
        point_to.edges_in.remove(self)

    @property
    def neighbors(self):
        return list(self._edges_out.keys())

    def weight(self, node: 'Node'):
        return self._edges_out[node]

    def set_weight(self, node: 'Node', weight):
        self._edges_out[node] = weight


class Tree:
    def __init__(self):
        self._root = None
        self._nodes = {}
        self._pts = []

    def addNode(self, key, value=None):
        k = f'n_{key}'
        if k not in self.__dict__:
            node = Node(key, value)
            if self._root is None:
                self._root = node

            self.__dict__[k] = node
        else:
            self.__dict__[k].value = value

        return self.__dict__[k]

    def drawEdge(self, node1: Node, node2: Node, weight=None, is_directed=True):
        node1.addEdge(node2, weight=weight)
        if is_directed:
            node1.addEdge(node2, weight=weight)
        else:
            try:
                w = iter(weight)
                node1.addEdge(node2, weight=w.__next__())
                node2.addEdge(node1, weight=w.__next__())

            except TypeError:
                node1.addEdge(node2, weight=weight)
                node2.addEdge(node1, weight=weight)

    def snap(self, node1: Node, node2: Node, is_directed=True):
        node1.breakEdge(node2)
        if not is_directed:
            node2.breakEdge(node1)

    @property
    def nodes(self):
        return [node for key, node in self.__dict__.items() if key[0:2] == 'n_']


def kruskal(tree: Tree):
    pq = PQ()  # Min Priority Queue
    pq.min()
    uf = UnionFind(set(tree.nodes))  # Union Find with Weighted Quick Union and Path Compression
    mst = Tree()  # Empty Tree to build Minimum Spanning Tree in

    # Initialize Priority Queue, Edge Weights are keys, nodes connected by edge are values
    nodes = tree.nodes
    for node in nodes:
        for edge in node.neighbors:
            pq.push(node.weight(edge), (node, edge))

    # Iterate through priority queue and add nodes to MST that doesn't cycle
    i = 0
    n = len(nodes) - 1
    while i < n:
        w, (a, b) = pq.pop
        if not uf.is_connected(a, b):
            n_a = mst.addNode(a.key, a.value)
            n_b = mst.addNode(b.key, b.value)
            mst.drawEdge(n_a, n_b, w)

            uf.union(a, b)
            i += 1

    return tree
