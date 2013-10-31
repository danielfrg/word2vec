# coding: utf-8
import scipy.linalg as LA


def unitvec(vec):
    return (1.0 / LA.norm(vec, ord=2)) * vec
