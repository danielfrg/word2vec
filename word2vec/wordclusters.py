# coding: utf-8
import numpy as np


class WordClusters(object):

    def __init__(self, vocab, clusters):
        self.vocab = vocab
        self.clusters = clusters

    def __getitem__(self, cluster):
        return self.vocab[self.clusters == cluster]
