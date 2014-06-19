import word2vec
import numpy as np


def load(fname, kind='bin', save_memory=True):
    '''
    Loads a word vectors file
    '''
    if kind == 'bin':
        return word2vec.WordVectors.from_binary(fname, save_memory=save_memory)
    elif kind == 'txt':
        return word2vec.WordVectors.from_text(fname, save_memory=save_memory)
    elif kind == 'mmap':
        return word2vec.WordVectors.from_mmap(fname)
    else:
        raise Exception('Unknown kind')


def load_clusters(fname):
    '''
    Loads a word cluster file
    '''
    return word2vec.WordClusters.from_text(fname)
