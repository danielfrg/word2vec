import itertools

import numpy as np
from sklearn.externals import joblib

from word2vec.utils import unitvec, distance


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

        # Used to make indexing faster
        self.vocab_hash = {}
        for i, word in enumerate(vocab):
            self.vocab_hash[word] = i

    def ix(self, word):
        """
        Returns the index on `self.vocab` and `self.vectors` for `word`
        """
        return self.vocab_hash[word]

    def word(self, ix):
        """Returns the word that corresponds to the index.

        Parameters
        -------
        ix : int
            The index of the word

        Returns
        -------
        str
            The word that corresponds to the index
        """
        return self.vocab[ix]

    def __getitem__(self, word):
        return self.get_vector(word)

    def __contains__(self, word):
        return word in self.vocab_hash

    def get_vector(self, word):
        """
        Returns the vector for a `word` in the vocabulary
        """
        return self.vectors[self.ix(word)]

    def distance(self, *args, **kwargs):
        """
        Compute the distance distance between two vectors or more (all combinations) of words

        Parameters
        ----------
        words : one or more words
        n : int (default 10)
            number of neighbors to return
        metric : string (default "cosine")
            What metric to use
        """
        metric = kwargs.get("metric", "cosine")    # Default is cosine

        combinations = list(itertools.combinations(args, r=2))

        ret = []
        for word1, word2 in combinations:
            dist = distance(self[word1], self[word2], metric=metric)
            ret.append((word1, word2, dist))
        return ret

    def closest(self, vector, n=10, metric="cosine"):
        """Returns the closest n words to a vector

        Parameters
        -------
        vector : numpy.array
        n : int (default 10)

        Returns
        -------
        Tuple of 2 numpy.array:
            1. position in self.vocab
            2. cosine similarity
        """
        distances = distance(self.vectors, vector, metric=metric)
        best = np.argsort(distances)[::-1][1:n + 1]
        best_metrics = distances[best]
        return best, best_metrics

    def similar(self, word, n=10, metric="cosine"):
        """
        Return similar words based on a metric

        Parameters
        ----------
        word : string
        n : int (default 10)

        Returns
        -------
        Tuple of 2 numpy.array:
            1. position in self.vocab
            2. cosine similarity
        """
        return self.closest(self[word], n=n, metric=metric)

    def analogy(self, pos, neg, n=10, metric="cosine"):
        """
        Analogy similarity.

        Parameters
        ----------
        pos : list
        neg : list

        Returns
        -------
        Tuple of 2 numpy.array:
            1. position in self.vocab
            2. cosine similarity

        Example
        -------
            `king - man + woman = queen` will be: `pos=['king', 'woman'], neg=['man']`
        """
        exclude = pos + neg
        pos = [(word, 1.0) for word in pos]
        neg = [(word, -1.0) for word in neg]

        mean = []
        for word, direction in pos + neg:
            mean.append(direction * self[word])
        mean = np.array(mean).mean(axis=0)

        metrics = distance(self.vectors, mean, metric=metric)
        best = metrics.argsort()[::-1][:n + len(exclude)]

        exclude_idx = [np.where(best == self.ix(word)) for word in exclude if self.ix(word) in best]
        new_best = np.delete(best, exclude_idx)
        best_metrics = metrics[new_best]
        return new_best[:n], best_metrics[:n]

    def generate_response(self, indexes, metrics, clusters=True):
        """
        Generates a pure python (no numpy) response based on numpy arrays
        returned by `self.cosine` and `self.analogy`
        """
        if self.clusters and clusters:
            return np.rec.fromarrays(
                (self.vocab[indexes], metrics, self.clusters.clusters[indexes]),
                names=("word", "metric", "cluster"),
            )
        else:
            return np.rec.fromarrays((self.vocab[indexes], metrics), names=("word", "metric"))

    def to_mmap(self, fname):
        joblib.dump(self, fname)

    @classmethod
    def from_binary(
            cls,
            fname,
            vocab_unicode_size=78,
            desired_vocab=None,
            encoding="utf-8",
            new_lines=True,
    ):
        """
        Create a WordVectors class based on a word2vec binary file

        Parameters
        ----------
        fname : path to file
        vocabUnicodeSize: the maximum string length (78, by default)
        desired_vocab: if set any words that don't fall into this vocab will be droped

        Returns
        -------
        WordVectors instance
        """
        with open(fname, "rb") as fin:
            # The first line has the vocab_size and the vector_size as text
            header = fin.readline()
            vocab_size, vector_size = list(map(int, header.split()))

            vocab = np.empty(vocab_size, dtype="<U%s" % vocab_unicode_size)
            vectors = np.empty((vocab_size, vector_size), dtype=np.float)
            binary_len = np.dtype(np.float32).itemsize * vector_size
            for i in range(vocab_size):
                # read word
                word = b""
                while True:
                    ch = fin.read(1)
                    if ch == b" ":
                        break
                    word += ch
                include = desired_vocab is None or word in desired_vocab
                if include:
                    vocab[i] = word.decode(encoding)

                # read vector
                vector = np.fromstring(fin.read(binary_len), dtype=np.float32)
                if include:
                    vectors[i] = unitvec(vector)
                if new_lines:
                    fin.read(1)    # newline char

            if desired_vocab is not None:
                vectors = vectors[vocab != "", :]
                vocab = vocab[vocab != ""]
        return cls(vocab=vocab, vectors=vectors)

    @classmethod
    def from_text(cls, fname, vocabUnicodeSize=78, desired_vocab=None, encoding="utf-8"):
        """
        Create a WordVectors class based on a word2vec text file

        Parameters
        ----------
        fname : path to file
        vocabUnicodeSize: the maximum string length (78, by default)
        desired_vocab: if set, this will ignore any word and vector that
                       doesn't fall inside desired_vocab.

        Returns
        -------
        WordVectors instance
        """
        with open(fname, "rb") as fin:
            header = fin.readline()
            vocab_size, vector_size = list(map(int, header.split()))

            vocab = np.empty(vocab_size, dtype="<U%s" % vocabUnicodeSize)
            vectors = np.empty((vocab_size, vector_size), dtype=np.float)
            for i, line in enumerate(fin):
                line = line.decode(encoding).rstrip()
                parts = line.split(" ")
                word = parts[0]
                include = desired_vocab is None or word in desired_vocab
                if include:
                    vector = np.array(parts[1:], dtype=np.float)
                    vocab[i] = word
                    vectors[i] = unitvec(vector)

            if desired_vocab is not None:
                vectors = vectors[vocab != "", :]
                vocab = vocab[vocab != ""]
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
        memmaped = joblib.load(fname, mmap_mode="r+")
        return cls(vocab=memmaped.vocab, vectors=memmaped.vectors)
