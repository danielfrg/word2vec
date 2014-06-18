import word2vec
import numpy as np


def load(fname, binary=True, save_memory=True):
    '''
    Loads a word vectors file
    '''
    if binary:
        return word2vec.WordVectors.from_binary(fname, save_memory=save_memory)
    else:
        return word2vec.WordVectors.from_text(fname, save_memory=save_memory)


def load_clusters(fname):
    '''
    Loads a word cluster file
    '''
    return word2vec.WordClusters.from_text(fname)
