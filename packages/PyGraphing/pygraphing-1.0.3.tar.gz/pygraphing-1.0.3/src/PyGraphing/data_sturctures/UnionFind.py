class UnionFind:
    def __init__(self, elements: set):
        self.sets = {el: el for el in elements}
        self.sizes = {el: 1 for el in elements}

    def union(self, set1, set2):
        """
        Weighted Quick Union with Path Compression.
        Makes the longer chain the parent of the shorter chain.
        O(log(N))
        """
        f1 = self.find(set1)
        f2 = self.find(set2)

        if f1 == f2:
            return

        if self.sizes[f1] < self.sizes[f2]:
            self.sets[f1] = f2
            self.sizes[f2] += self.sizes[f1]

        else:
            self.sets[f2] = f1
            self.sizes[f1] += self.sizes[f2]

    def find(self, val):
        """
        Finds the top node in the set that houses the node given by val
        O(log(N))
        """
        indices = []
        while val != self.sets[val]:
            indices.append(val)
            val = self.sets[val]

        for s in indices:
            self.sets[s] = val

        return val

    def is_connected(self, node1, node2):
        return self.find(node1) == self.find(node2)

    def compress(self):
        _ = [self.find(el) for el in self.sets]

    def unique_sets(self):
        self.compress()
        return [{item for item, s in self.sets.items() if s == i} for i in set(self.sets.values())]
