from __future__ import division, print_function, unicode_literals

import numpy as np


def unitvec(vec):
    return (1.0 / np.linalg.norm(vec, ord=2)) * vec


def distance(a, b, metric="dot"):
    """
    Calculate distance between two vectors based on a Metric

    Metrics:
    1. dot product. Note that in word2vec all the norms are 1 so the dot product is basically the same as cosine distance
    """
    if metric == "dot":
        return np.dot(a, b.T)
    raise Exception(f"Unknown metric '{metric}'")
