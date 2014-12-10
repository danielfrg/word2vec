from __future__ import unicode_literals

import os
import sys
import subprocess


def word2vec(train, output, size=100, window=5, sample='1e-3', hs=0, negative=5,
             threads=12, iter_=5, min_count=5, alpha=0.025, debug=2, binary=1,
             cbow=1,
             save_vocab=None, read_vocab=None, verbose=False):
    process = ['word2vec']
    args = ['-train', '-output', '-size', '-window', '-sample', '-hs',
            '-negative', '-threads', '-iter', '-min-count', '-alpha', '-debug',
            '-binary', '-cbow']
    values = [train, output, size, window, sample, hs, negative, threads, iter_,
              min_count, alpha, debug, binary, cbow]

    for arg, value in zip(args, values):
        process.append(arg)
        process.append(unicode(value))
    if save_vocab is not None:
        process.append('-save-vocab')
        process.append(unicode(save_vocab))
    if read_vocab is not None:
        process.append('-read-vocab')
        process.append(unicode(read_vocab))

    proc = subprocess.Popen(process, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if verbose:
        for line in proc.stdout:
            sys.stdout.write(line)
            if 'ERROR:' in line:
                raise Exception(line)
            sys.stdout.flush()

    out, err = proc.communicate()


def word2clusters(train, output, classes, size=100, window=5, sample='1e-3',
                  hs=0, negative=5, threads=12, iter_=5, min_count=5,
                  alpha=0.025, debug=2, binary=1, cbow=1,
                  save_vocab=None, read_vocab=None, verbose=False):
    process = ['word2vec']
    args = ['-train', '-output', '-size', '-window', '-sample', '-hs',
            '-negative', '-threads', '-iter', '-min-count', '-alpha', '-debug',
            '-binary', '-cbow', '-classes']
    values = [train, output, size, window, sample, hs, negative, threads, iter_,
              min_count, alpha, debug, binary, cbow, classes]
    for arg, value in zip(args, values):
        process.append(arg)
        process.append(unicode(value))
    if save_vocab is not None:
        process.append('-save-vocab')
        process.append(unicode(save_vocab))
    if read_vocab is not None:
        process.append('-read-vocab')
        process.append(unicode(read_vocab))

    proc = subprocess.Popen(process, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if verbose:
        for line in proc.stdout:
            sys.stdout.write(line)
            if 'ERROR:' in line:
                raise Exception(line)
            sys.stdout.flush()


def word2phrase(train, output, min_count=5, threshold=100, debug=2, verbose=False):
    process = ['word2phrase']
    args = ['-train', '-output', '-min-count', '-threshold', '-debug']
    values = [train, output, min_count, threshold, debug]
    for arg, value in zip(args, values):
        process.append(arg)
        process.append(value)

    proc = subprocess.Popen(process, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if verbose:
        for line in proc.stdout:
            sys.stdout.write(line)
            if 'ERROR:' in line:
                raise Exception(line)
            sys.stdout.flush()
