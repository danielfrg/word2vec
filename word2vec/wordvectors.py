from __future__ import unicode_literals

import numpy as np
try:
    from sklearn.externals import joblib
except:
    joblib = None

from word2vec.utils import unitvec


class WordVectors(object):

    def __init__(self, vocab, vectors, clusters=None):
        """
        Initialize a WordVectors class based on vocabulary and vectors

        This initializer precomputes the vectors of the vectors

        Parameters
        ----------
        vocab : np.array
            1d array with the vocabulary
        vectors : np.array
            2d array with the vectors calculated by word2vec
        clusters : word2vec.WordClusters (optional)
            1d array with the clusters calculated by word2vec
        """
        self.vocab = vocab
        self.vectors = vectors
        self.clusters = clusters

    def ix(self, word):
        """
        Returns the index on self.vocab and `self.vectors` for `word`
        """
        temp = np.where(self.vocab == word)[0]
        if temp.size == 0:
            raise KeyError('Word not in vocabulary')
        else:
            return temp[0]

    def __getitem__(self, word):
        return self.get_vector(word)

    def __contains__(self, word):
        return word in self.vocab

    def get_vector(self, word):
        """
        Returns the (vectors) vector for `word` in the vocabulary
        """
        idx = self.ix(word)
        return self.vectors[idx]

    def cosine(self, word, n=10):
        """
        Cosine similarity.

        metric = dot(vectors_of_vectors, vectors_of_target_vector)
        Uses a precomputed vectors of the vectors

        Parameters
        ----------
        word : string
        n : int, optional (default 10)
            number of neighbors to return

        Returns
        -------
        2 numpy.array:
            1. position in self.vocab
            2. cosine similarity
        """
        metrics = np.dot(self.vectors, self[word].T)
        best = np.argsort(metrics)[::-1][1:n+1]
        best_metrics = metrics[best]
        return best, best_metrics

    def analogy(self, pos, neg, n=10):
        """
        Analogy similarity.

        Parameters
        ----------
        pos : list
        neg : list

        Returns
        -------
        2 numpy.array:
            1. position in self.vocab
            2. cosine similarity

        Example
        -------
            `king - man + woman = queen` will be:
            `pos=['king', 'woman'], neg=['man']`
        """
        exclude = pos + neg
        pos = [(word, 1.0) for word in pos]
        neg = [(word, -1.0) for word in neg]

        mean = []
        for word, direction in pos + neg:
            mean.append(direction * self[word])
        mean = np.array(mean).mean(axis=0)

        metrics = np.dot(self.vectors, mean)
        best = metrics.argsort()[::-1][:n + len(exclude)]

        exclude_idx = [np.where(best == self.ix(word)) for word in exclude if self.ix(word) in best]
        new_best = np.delete(best, exclude_idx)
        best_metrics = metrics[new_best]
        return new_best[:n], best_metrics[:n]

    def generate_response(self, indexes, metrics, clusters=True):
        '''
        Generates a pure python (no numpy) response based on numpy arrays
        returned by `self.cosine` and `self.analogy`
        '''
        if self.clusters and clusters:
            return np.rec.fromarrays((self.vocab[indexes], metrics, self.clusters.clusters[indexes]), names=('word', 'metric', 'cluster'))
        else:
            return np.rec.fromarrays((self.vocab[indexes], metrics), names=('word', 'metric'))

    def to_mmap(self, fname):
        if not joblib:
            raise Exception("sklearn is needed to save as mmap")

        joblib.dump(self, fname)

    @classmethod
    def from_binary(cls, fname, vocabUnicodeSize=78, desired_vocab=None):
        """
        Create a WordVectors class based on a word2vec binary file

        Parameters
        ----------
        fname : path to file
        vocabUnicodeSize: the maximum string length (78, by default)
        desired_vocab: if set, this will ignore any word and vector that doesn't fall inside desired_vocab.

        Returns
        -------
        WordVectors instance
        """
        with open(fname) as fin:
            header = fin.readline()
            vocab_size, vector_size = map(int, header.split())

            vocab = np.empty(vocab_size, dtype='<U%s' % vocabUnicodeSize)
            vectors = np.empty((vocab_size, vector_size), dtype=np.float)
            binary_len = np.dtype(np.float32).itemsize * vector_size
            for i in xrange(vocab_size):
                # read word
                word = ''
                while True:
                    ch = fin.read(1).decode('ISO-8859-1')
                    if ch == ' ':
                        break
                    word += ch
                include = desired_vocab is None or word in desired_vocab
                if include:
                    vocab[i] = word

                # read vector
                vector = np.fromstring(fin.read(binary_len), dtype=np.float32)
                if include:
                    vectors[i] = unitvec(vector)
                fin.read(1)  # newline

            if desired_vocab is not None:
                vectors = vectors[vocab != u'', :]
                vocab = vocab[vocab != u'']
        return cls(vocab=vocab, vectors=vectors)

    @classmethod
    def from_text(cls, fname, vocabUnicodeSize=78, desired_vocab=None):
        """
        Create a WordVectors class based on a word2vec text file

        Parameters
        ----------
        fname : path to file
        vocabUnicodeSize: the maximum string length (78, by default)
        desired_vocab: if set, this will ignore any word and vector that doesn't fall inside desired_vocab.

        Returns
        -------
        WordVectors instance
        """
        with open(fname) as fin:
            header = fin.readline()
            vocab_size, vector_size = map(int, header.split())

            vocab = np.empty(vocab_size, dtype='<U%s' % vocabUnicodeSize)
            vectors = np.empty((vocab_size, vector_size), dtype=np.float)
            for i, line in enumerate(fin):
                line = line.decode('ISO-8859-1').strip()
                parts = line.split(' ')
                word = parts[0]
                include = desired_vocab is None or word in desired_vocab
                if include:
                    vector = np.array(parts[1:], dtype=np.float)
                    vocab[i] = word
                    vectors[i] = unitvec(vector)

            if desired_vocab is not None:
                vectors = vectors[vocab != u'', :]
                vocab = vocab[vocab != u'']
        return cls(vocab=vocab, vectors=vectors)

    @classmethod
    def from_mmap(cls, fname):
        """
        Create a WordVectors class from a memory map

        Parameters
        ----------
        fname : path to file

        Returns
        -------
        WordVectors instance
        """
        memmaped = joblib.load(fname, mmap_mode='r+')
        return cls(vocab=memmaped.vocab, vectors=memmaped.vectors)
