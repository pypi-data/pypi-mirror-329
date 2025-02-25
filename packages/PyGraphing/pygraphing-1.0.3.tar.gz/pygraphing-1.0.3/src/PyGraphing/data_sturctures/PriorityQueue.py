from collections import namedtuple

Item = namedtuple('Item', ('key', 'value'))


class Heap(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().insert(0, None)

        self.is_min = False

        if self.n > 1:
            self._floyd_heapify()

    def _pred(self, left, rght):
        if self.is_min:
            return left > rght
        else:
            return left < rght

    @property
    def n(self):
        return len(self) - 1

    def xchg(self, i, j):
        temp = self[i]
        self[i] = self[j]
        self[j] = temp

    def swim(self, k):
        while k > 1 and self._pred(self[k // 2].key, self[k].key):
            self.xchg(k // 2, k)
            k //= 2

    def sink(self, k, n=-1):
        if n == -1:
            n = self.n

        j = 2 * k
        while j <= n:
            if j < n:
                if self._pred(self[j].key, self[j + 1].key):
                    j += 1

            if self._pred(self[j].key, self[k].key):
                break

            self.xchg(k, j)

            k = j
            j = 2 * k

    def insert(self, key, value):
        item = Item(key=key, value=value)
        self.append(item)
        self.swim(self.n)

    def _floyd_heapify(self):
        for i in range(self.n // 2, 0, -1):
            self.sink(i, n=self.n)

    def __str__(self):
        return str([str(i.value) for i in self[1:]])


class PQ:
    def __init__(self):
        self._heap = Heap()

    def min(self):
        self._heap.is_min = True
        return

    def max(self):
        self._heap.is_min = False
        return

    def pop(self):
        self._heap.xchg(1, -1)
        item = self._heap.pop(-1)
        self._heap.sink(1)

        return item.value

    def push(self, key, value):
        self._heap.insert(key=key, value=value)

    def __str__(self):
        return str(self._heap)
