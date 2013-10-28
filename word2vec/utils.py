# coding: utf-8


class TopItems(object):
    '''
    Class that mantains the top (n) items based on a similarity value.
    Smaller values are considered better and therefore mantained.

    Usage
    -----
    top = TopItems(10)

    '''

    def __init__(self, size, items=None, distances=None, init_dist=1e6):
        self.size = size
        if distances is not None and items is not None:
            self.distances = distances
            self.items = items
        else:
            self.distances = [init_dist for i in range(size)]
            self.items = [None for i in range(size)]

    def insert(self, n_item, n_dist):
        if n_dist < max(self.distances):
            if n_dist < min(self.distances):
                self.distances.insert(0, n_dist)
                self.distances = self.distances[:self.size]
                self.items.insert(0, n_item)
                self.items = self.items[:self.size]
            else:
                for i, dist_1 in enumerate(reversed(self.distances[:-1])):
                    dist_2 = self.distances[self.size - i - 1]
                    if n_dist < dist_2 and n_dist >= dist_1:
                        self.distances.insert(self.size - i - 1, n_dist)
                        self.distances = self.distances[:self.size]
                        self.items.insert(self.size - i - 1, n_item)
                        self.items = self.items[:self.size]
                        break
