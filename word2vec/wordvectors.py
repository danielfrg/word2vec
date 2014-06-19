import numpy as np
try:
    from sklearn.externals import joblib
except:
    joblib = None

from word2vec.utils import unitvec


class WordVectors(object):

    def __init__(self, vocab, vectors=None, l2norm=None, save_memory=True):
        """
        Initialize a WordVectors class based on vocabulary and vectors

        This initializer precomputes the l2norm of the vectors

        Parameters
        ----------
        vocab : np.array
            1d array with the vocabulary
        vectors : np.array
            2d array with the vectors calculated by word2vec
        l2norm : np.array
            2d array with the calulated l2norm of the vectors
        save_memory : boolean
            wheter or not save the original vectors in `self.vectors`
        """
        if vectors is None and l2norm is None:
            raise Exception('Need vectors OR l2norm arguments')

        self.vocab = vocab

        if l2norm is None:
            if not save_memory:
                self.vectors = vectors
            self.l2norm = np.vstack(unitvec(vec) for vec in vectors)
        else:
            self.l2norm = l2norm

    def ix(self, word):
        """
        Returns the index on self.vocab and self.l2norm for `word`
        """
        temp = np.where(self.vocab == word)[0]
        if temp.size == 0:
            raise KeyError('Word not in vocabulary')
        else:
            return temp[0]

    def get_vector(self, word):
        """
        Returns the (l2norm) vector for `word` in the vocabulary
        """
        idx = self.ix(word)
        return self.l2norm[idx]

    def __getitem__(self, word):
        return self.get_vector(word)

    def generate_response(self, indexes, metric, exclude=''):
        """
        Generates a response as a list of tuples based on the indexes
        Each tuple is: (vocab[i], metric[i])
        """
        if isinstance(exclude, basestring):
            exclude = [exclude]
        return [(word, sim) for word, sim in zip(self.vocab[indexes], metric[indexes]) if word not in exclude]

    def cosine(self, words, n=10):
        """
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
        dict: of list of tuples

        Example
        -------
        >>> model.cosine('black', n=2)
        ```
        ```
        {'black': [('white', 0.94757425919916516),
                   ('yellow', 0.94640807944950878)]
        }
        """
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
        """
        Test method for cosine distance using `scipy.distance.cosine`

        Note: This method is **a lot** slower than `self.cosine`
        and results are the almost the same, you should be using `self.cosine`

        Requires: `__init__(..., save_memory=False)`

        Parameters
        ----------
        word : string
            word in the vocabulary to calculate the vectors
        n : int, optional (default 10)
            number of neighbors to return
        """
        from scipy.spatial import distance

        target_vec = self[word]
        metric = np.empty(self.vocab.shape)
        for idx, vector in enumerate(self.vectors):
            metric[idx] = distance.cosine(target_vec, vector)
        best = metric.argsort()[:n + 1]

        return self.generate_response(best, metric, exclude=word)

    def analogy(self, pos, neg, n=10):
        """
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
        """
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

    def to_mmap(self, fname):
        if not joblib:
            raise Exception("sklearn needed for save as mmap")

        joblib.dump(self, fname)

    @classmethod
    def from_binary(cls, fname, save_memory=True):
        """
        Create a WordVectors class based on a word2vec binary file

        Parameters
        ----------
        fname : path to file
        save_memory : boolean

        Returns
        -------
        WordVectors class
        """
        with open(fname) as fin:
            header = fin.readline()
            vocab_size, vector_size = map(int, header.split())
            vocab = []

            vectors = np.empty((vocab_size, vector_size), dtype=np.float)
            binary_len = np.dtype(np.float32).itemsize * vector_size
            for line_number in xrange(vocab_size):
                # mixed text and binary: read text first, then binary
                word = ''
                while True:
                    ch = fin.read(1)
                    if ch == ' ':
                        break
                    word += ch
                vocab.append(word)

                vector = np.fromstring(fin.read(binary_len), np.float32)
                vectors[line_number] = vector
                fin.read(1)  # newline
        vocab = np.array(vocab)

        return cls(vocab=vocab, vectors=vectors, save_memory=save_memory)

    @classmethod
    def from_text(cls, fname, save_memory=True):
        """
        Create a WordVectors class based on a word2vec text file

        Parameters
        ----------
        fname : path to file
        save_memory : boolean

        Returns
        -------
        WordVectors class
        """
        with open(fname) as f:
            parts = f.readline().strip().split(' ')
            shape = int(parts[0]), int(parts[1])

        vocab = np.genfromtxt(fname, dtype=object, delimiter=' ', usecols=0, skip_header=1)

        cols = np.arange(1, shape[1] + 1)
        vectors = np.genfromtxt(fname, dtype=float, delimiter=' ', usecols=cols, skip_header=1)

        return cls(vocab=vocab, vectors=vectors, save_memory=save_memory)

    @classmethod
    def from_mmap(cls, fname):
        """
        Create a WordVectors class from a memory map

        Parameters
        ----------
        fname : path to file
        save_memory : boolean

        Returns
        -------
        WordVectors class
        """
        memmaped = joblib.load(fname, mmap_mode='r+')
        return cls(vocab=memmaped.vocab, l2norm=memmaped.l2norm)
