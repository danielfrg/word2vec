# coding: utf-8
import numpy as np
from word2vec.utils import unitvec


class WordVectors(object):

    def __init__(self, vocab=None, vectors=None, saveMemory=True):
        self.vocab = vocab
        if not saveMemory:
            self.vectors = vectors
        self.l2norm = np.vstack(unitvec(vec) for vec in vectors)

    def ix(self, word):
        '''
        Returns the index on self.vocab and self.l2norm for `word`
        '''
        temp = np.where(self.vocab == word)[0]
        if temp.size == 0:
            raise KeyError('Word not in vocabulary')
        else:
            return temp[0]

    def get_vector(self, word):
        '''
        Returns the (l2norm) vector for `word` in the vocabulary
        '''
        idx = self.ix(word)
        return self.l2norm[idx]

    def __getitem__(self, word):
        return self.get_vector(word)

    def generate_response(self, indexes, metric, exclude=''):
        '''
        Generates a response as a list of tuples based on the indexes
        Each tuple is: (vocab[i], metric[i])
        '''
        if isinstance(exclude, basestring):
            exclude = [exclude]
        return [(word, sim) for word, sim in zip(self.vocab[indexes], metric[indexes]) if word not in exclude]

    def cosine(self, words, n=10):
        '''
        Cosine similarity.

        metric = dot(l2norm_of_vectors, l2norm_of_target_vector)
        Uses a precomputed l2norm of the vectors

        Parameters
        ----------
        words : string or list of string
            word(s) in the vocabulary to calculate the vectors
        n : int, optional (default 10)
            number of neighbors to return

        Returns
        -------
        dict: with the n similar words and its similarity as a list of tuples

        Example
        -------
        >>> model.cosine('black', n=2)
        ```
        ```
        {'black': [('white', 0.94757425919916516),
                   ('yellow', 0.94640807944950878)]
        }
        '''
        if isinstance(words, basestring):
            words = [words]

        targets = np.vstack((self.get_vector(word) for word in words))
        metrics = np.dot(self.l2norm, targets.T)

        ans = {}
        for col, word in enumerate(words):
            best = np.argsort(metrics[:, col])[::-1][:n + 1]
            best = self.generate_response(best, metrics[:, col], exclude=word)
            ans[word] = best

        return ans

    def _cosine(self, word, n=10):
        '''
        Cosine distance using scipy.distance.cosine

        Note: This method is **a lot** slower than `self.cosine`
        and results are the almost the same, really just use `self.cosine`
        This is just available for testing.

        Requires: `__init__(..., saveMemory=False)`

        Parameters
        ----------
        word : string
            word in the vocabulary to calculate the vectors
        n : int, optional (default 10)
            number of neighbors to return
        '''
        from scipy.spatial import distance
        target_vec = self[word]
        metric = np.empty(self.vocab.shape)
        for idx, vector in enumerate(self.vectors):
            metric[idx] = distance.cosine(target_vec, vector)

        best = metric.argsort()[:n + 1]
        return self.generate_response(best, metric, exclude=word)

    def analogy(self, pos, neg, n=10):
        '''
        Analogy similarity.

        Parameters
        ----------
        pos : list
        neg : list

        Returns
        -------
        List of tuples, each tuple is  (word, similarity)


        Example
        -------
            `king - man + woman = queen` will be:
            `pos=['king', 'woman'], neg=['man']`
        '''
        words = pos + neg

        pos = [(word, 1.0) for word in pos]
        neg = [(word, -1.0) for word in neg]

        mean = []
        for word, direction in pos + neg:
            mean.append(direction * unitvec(self.get_vector(word)))
        mean = np.array(mean).mean(axis=0)

        similarities = np.dot(self.l2norm, mean)
        best = similarities.argsort()[::-1][:n + len(words) - 1]
        return self.generate_response(best, similarities, exclude=words)
