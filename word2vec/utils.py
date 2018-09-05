import numpy as np


def unitvec(vec):
    return (1.0 / np.linalg.norm(vec, ord=2)) * vec


def distance(a, b, metric="cosine"):
    """
    Calculate distance between two vectors based on a Metric

    Metrics:
    1. cosine distance. Note that in word2vec all the norms are 1 so the dot product is the same as cosine distance
    """
    if metric == "cosine":
        return np.dot(a, b.T)
    raise Exception("Unknown metric '{metric}'".format(metric=metric))
