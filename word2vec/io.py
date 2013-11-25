# coding: utf-8
import word2vec
import numpy as np


def load(fname, binary=True, saveMemory=True):
    '''
    Loads a word vectors binary file

    load with binary=True was gracefully copied from gensim:
    http://github.com/piskvorky/gensim/blob/develop/gensim/models/word2vec.py
    '''
    if binary:
        vocab = []
        vectors = None

        with open(fname) as fin:
            header = fin.readline()
            vocab_size, vector_size = map(int, header.split())

            vectors = np.empty((vocab_size, vector_size), dtype=np.float)
            binary_len = np.dtype(np.float32).itemsize * vector_size
            for line_no in xrange(vocab_size):
                # mixed text and binary: read text first, then binary
                word = ''
                while True:
                    ch = fin.read(1)
                    if ch == ' ':
                        break
                    word += ch
                vocab.append(word)

                vector = np.fromstring(fin.read(binary_len), np.float32)
                vectors[line_no] = vector
                fin.read(1)  # newline
        vocab = np.array(vocab)

        return word2vec.WordVectors(vocab=vocab, vectors=vectors, saveMemory=saveMemory)
    else:
        shape = tuple()
        with open(fname) as f:
            parts = f.readline().strip().split(' ')
            shape = int(parts[0]), int(parts[1])

        vocab = np.genfromtxt(fname, dtype=object, delimiter=' ', usecols=0, skip_header=1)

        cols = np.arange(1, shape[1] + 1)
        vectors = np.genfromtxt(fname, dtype=float, delimiter=' ', usecols=cols, skip_header=1)
        return word2vec.WordVectors(vocab=vocab, vectors=vectors)


def load_clusters(fname):
    vocab = np.genfromtxt(fname, dtype=np.object, delimiter=' ', usecols=0)
    clusters = np.genfromtxt(fname, dtype=int, delimiter=' ', usecols=1)
    return word2vec.WordClusters(vocab=vocab, clusters=clusters)
