import numpy as np


class WordClusters(object):

    def __init__(self, vocab, clusters):
        self.vocab = vocab
        self.clusters = clusters

    def __getitem__(self, cluster):
        return self.vocab[self.clusters == cluster]

    @classmethod
    def from_text(cls, fname):
        vocab = np.genfromtxt(fname, dtype=np.object, delimiter=' ', usecols=0)
        clusters = np.genfromtxt(fname, dtype=int, delimiter=' ', usecols=1)
        return cls(vocab=vocab, clusters=clusters)
