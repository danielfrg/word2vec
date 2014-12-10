from __future__ import unicode_literals

from numpy import linalg as LA


def unitvec(vec):
    return (1.0 / LA.norm(vec, ord=2)) * vec
