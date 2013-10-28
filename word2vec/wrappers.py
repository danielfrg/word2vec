# coding: utf-8
import numpy as np
from scipy.spatial import distance
from word2vec.utils import TopItems


class WordVectors(object):

    def __init__(self, vocab=None, vectors=None):
        self.vocab = vocab
        self.vectors = vectors

    def dot(self, word, n=10):
        '''
        Calculate distance based only on the dot product.
        This is the faster calculation possible and usually gives good results.
        '''
        word_idx = np.where(self.vocab == word)[0][0]
        distances = np.dot(self.vectors[word_idx], self.vectors.T)
        best = distances.argsort()[::-1][:n + 1]
        return [(_word, dist) for _word, dist in zip(self.vocab[best], distances[best]) if _word != word]

    def cosine(self, word, n=10):
        '''
        Calculate distance based only on the cosine distance

        Note: If the size of the vectors and vocabulary is to big and this fails
        try cosie_lm
        '''
        word_idx = np.where(self.vocab == word)[0][0]
        distances = np.empty(self.vocab.shape)
        target_vec = self.vectors[word_idx]
        for idx, vector in enumerate(self.vectors):
            distances[idx] = distance.cosine(target_vec, vector)

        best = distances.argsort()[:n + 1]
        return [(_word, dist) for _word, dist in zip(self.vocab[best], distances[best]) if _word != word]

    def cosine_lm(self, word, n=10):
        '''
        Calculate distance based only on the cosine distance (light memory edition).
        Uses an algorithm that does not keep in memory all the distances so
        uses less memory, on the other hand is a little bit slower.
        '''
        word_idx = np.where(self.vocab == word)[0][0]
        target_vec = self.vectors[word_idx]
        ol = TopItems(n)
        for _word, vector in zip(self.vocab, self.vectors):
            if word != _word:
                dist = distance.cosine(target_vec, vector)
                ol.insert(_word, dist)
        return [(word, dist) for word, dist in zip(ol.items, ol.distances)]


class WordClusters(object):
    def __init__(self, fname=None):
        if fname is not None:
            self.load(fname)

    def load(self, fname):
        self.words = np.genfromtxt(fname, dtype=object, delimiter=' ', usecols=0)
        self.clusters = np.genfromtxt(fname, dtype=int, delimiter=' ', usecols=1)
