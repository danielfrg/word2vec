import word2vec
import numpy as np


def load(fname, binary=True, saveMemory=True):
    '''
    Loads a word vectors file
    '''
    if binary:
        return word2vec.WordVectors.from_binary(fname, saveMemory=saveMemory)
    else:
        return word2vec.WordVectors.from_text(fname, saveMemory=saveMemory)


def load_clusters(fname):
    '''
    Loads a word cluster file
    '''
    return word2vec.WordClusters.from_text(fname)
