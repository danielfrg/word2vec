from __future__ import division, print_function, unicode_literals

import word2vec


def load(fname, kind='auto', *args, **kwargs):
    '''
    Loads a word vectors file
    '''
    if kind == 'auto':
        if fname.endswith('.bin'):
            kind = 'bin'
        elif fname.endswith('.txt'):
            kind = 'txt'
        else:
            raise Exception('Could not identify kind')
    if kind == 'bin':
        return word2vec.WordVectors.from_binary(fname, *args, **kwargs)
    elif kind == 'txt':
        return word2vec.WordVectors.from_text(fname, *args, **kwargs)
    elif kind == 'mmap':
        return word2vec.WordVectors.from_mmap(fname, *args, **kwargs)
    else:
        raise Exception('Unknown kind')


def load_clusters(fname):
    '''
    Loads a word cluster file
    '''
    return word2vec.WordClusters.from_text(fname)
