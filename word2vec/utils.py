# coding: utf-8
import numpy as np
from scipy.spatial.distance import cosine


class TopWords(object):

    def __init__(self, size, distances=None, values=None, init_dist=1e6):
        self.size = size
        if distances is not None:
            self.distances = distances
            self.values = values
        else:
            self.distances = [init_dist for i in range(size)]
            self.values = [None for i in range(size)]

    def insert(self, n_dist, n_value):
        if n_dist < max(self.distances):
            if n_dist < min(self.distances):
                self.distances.insert(0, n_dist)
                self.distances = self.distances[:self.size]
                self.values.insert(0, n_value)
                self.values = self.values[:self.size]
            else:
                for i, dist_1 in enumerate(reversed(self.distances[:-1])):
                    dist_2 = self.distances[self.size - i - 1]
                    if n_dist < dist_2 and n_dist >= dist_1:
                        self.distances.insert(self.size - i - 1, n_dist)
                        self.distances = self.distances[:self.size]
                        self.values.insert(self.size - i - 1, n_value)
                        self.values = self.values[:self.size]
                        break


def neighbors(wv, target, n=10):
    word_ix = np.where(wv.words == target)[0]
    ol = TopWords(n)
    for word, vector in zip(wv.words, wv.vectors[:]):
        if word != target:
            dist = cosine(wv.vectors[word_ix, :], vector)
            ol.insert(dist, word)
    return ol
