from __future__ import division, print_function, unicode_literals

import numpy as np


class WordClusters(object):

    def __init__(self, vocab, clusters):
        self.vocab = vocab
        self.clusters = clusters

    def ix(self, word):
        """
        Returns the index on self.vocab and self.clusters for `word`
        """
        temp = np.where(self.vocab == word)[0]
        if temp.size == 0:
            raise KeyError('Word not in vocabulary')
        else:
            return temp[0]

    def __getitem__(self, word):
        return self.get_cluster(word)

    def get_cluster(self, word):
        """
        Returns the cluster number for a word in the vocabulary
        """
        idx = self.ix(word)
        return self.clusters[idx]

    def get_words_on_cluster(self, cluster):
        return self.vocab[self.clusters == cluster]

    @classmethod
    def from_text(cls, fname):
        vocab = np.genfromtxt(fname, dtype=np.object, delimiter=' ', usecols=0)
        clusters = np.genfromtxt(fname, dtype=int, delimiter=' ', usecols=1)
        return cls(vocab=vocab, clusters=clusters)
