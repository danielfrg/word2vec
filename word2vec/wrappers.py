# coding: utf-8
import numpy as np
from word2vec.utils import neighbors


class WordVectors(object):

    def __init__(self, fname=None):
        if fname is not None:
            self.load(fname)

    def load(self, fname):
        with open(fname) as f:
            parts = f.readline().strip().split(' ')
            self.shape = int(parts[0]), int(parts[1])

        self.words = np.genfromtxt(fname, dtype=object, delimiter=' ', usecols=0, skip_header=1)

        cols = np.arange(1, self.shape[1] + 1)
        self.vectors = np.genfromtxt(fname, dtype=float, delimiter=' ', usecols=cols, skip_header=1)

    def neighbors(self, word, n=10):
        return neighbors(self, word, n)


class WordClusters(object):
    def __init__(self, fname=None):
        if fname is not None:
            self.load(fname)

    def load(self, fname):
        self.words = np.genfromtxt(fname, dtype=object, delimiter=' ', usecols=0)
        self.clusters = np.genfromtxt(fname, dtype=int, delimiter=' ', usecols=1)


if __name__ == '__main__':
    wv = WordClusters('text8-clusters.txt')
    print wv.clusters
