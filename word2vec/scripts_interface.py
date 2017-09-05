from __future__ import division, print_function, unicode_literals

import sys
import subprocess


def word2vec(train, output, size=100, window=5, sample='1e-3', hs=0,
             negative=5, threads=12, iter_=5, min_count=5, alpha=0.025,
             debug=2, binary=1, cbow=1, save_vocab=None, read_vocab=None,
             verbose=False):
    """
    word2vec execution

    Parameters for training:
        train <file>
            Use text data from <file> to train the model
        output <file>
            Use <file> to save the resulting word vectors / word clusters
        size <int>
            Set size of word vectors; default is 100
        window <int>
            Set max skip length between words; default is 5
        sample <float>
            Set threshold for occurrence of words. Those that appear with
            higher frequency in the training data will be randomly
            down-sampled; default is 0 (off), useful value is 1e-5
        hs <int>
            Use Hierarchical Softmax; default is 1 (0 = not used)
        negative <int>
            Number of negative examples; default is 0, common values are 5 - 10
            (0 = not used)
        threads <int>
            Use <int> threads (default 1)
        min_count <int>
            This will discard words that appear less than <int> times; default
            is 5
        alpha <float>
            Set the starting learning rate; default is 0.025
        debug <int>
            Set the debug mode (default = 2 = more info during training)
        binary <int>
            Save the resulting vectors in binary moded; default is 0 (off)
        cbow <int>
            Use the continuous back of words model; default is 1 (use 0 for
            skip-gram model)
        save_vocab <file>
            The vocabulary will be saved to <file>
        read_vocab <file>
            The vocabulary will be read from <file>, not constructed from the
            training data
        verbose
            Print output from training
    """
    command = ['word2vec']
    args = ['-train', '-output', '-size', '-window', '-sample', '-hs',
            '-negative', '-threads', '-iter', '-min-count', '-alpha', '-debug',
            '-binary', '-cbow']
    values = [train, output, size, window, sample, hs, negative, threads,
              iter_, min_count, alpha, debug, binary, cbow]

    for arg, value in zip(args, values):
        command.append(arg)
        command.append(str(value))
    if save_vocab is not None:
        command.append('-save-vocab')
        command.append(str(save_vocab))
    if read_vocab is not None:
        command.append('-read-vocab')
        command.append(str(read_vocab))

    run_cmd(command, verbose=verbose)


def word2clusters(train, output, classes, size=100, window=5, sample='1e-3',
                  hs=0, negative=5, threads=12, iter_=5, min_count=5,
                  alpha=0.025, debug=2, binary=1, cbow=1,
                  save_vocab=None, read_vocab=None, verbose=False):
    command = ['word2vec']

    args = ['-train', '-output', '-size', '-window', '-sample', '-hs',
            '-negative', '-threads', '-iter', '-min-count', '-alpha', '-debug',
            '-binary', '-cbow', '-classes']
    values = [train, output, size, window, sample, hs, negative, threads,
              iter_, min_count, alpha, debug, binary, cbow, classes]

    for arg, value in zip(args, values):
        command.append(arg)
        command.append(str(value))

    if save_vocab is not None:
        command.append('-save-vocab')
        command.append(str(save_vocab))
    if read_vocab is not None:
        command.append('-read-vocab')
        command.append(str(read_vocab))

    run_cmd(command, verbose=verbose)


def word2phrase(train, output, min_count=5, threshold=100, debug=2,
                verbose=False):
    command = ['word2phrase']

    args = ['-train', '-output', '-min-count', '-threshold', '-debug']
    values = [train, output, min_count, threshold, debug]
    for arg, value in zip(args, values):
        command.append(arg)
        command.append(str(value))

    run_cmd(command, verbose=verbose)


def doc2vec(train, output, size=100, window=5, sample='1e-3', hs=0, negative=5,
            threads=12, iter_=5, min_count=5, alpha=0.025, debug=2, binary=1,
            cbow=1,
            save_vocab=None, read_vocab=None, verbose=False):
    command = ['word2vec-doc2vec']
    args = ['-train', '-output', '-size', '-window', '-sample', '-hs',
            '-negative', '-threads', '-iter', '-min-count', '-alpha',
            '-debug', '-binary', '-cbow']
    values = [train, output, size, window, sample, hs, negative, threads,
              iter_, min_count, alpha, debug, binary, cbow]

    for arg, value in zip(args, values):
        command.append(arg)
        command.append(str(value))
    if save_vocab is not None:
        command.append('-save-vocab')
        command.append(str(save_vocab))
    if read_vocab is not None:
        command.append('-read-vocab')
        command.append(str(read_vocab))

    command.append('sentence-vectors')
    command.append('1')

    run_cmd(command, verbose=verbose)


def run_cmd(command, verbose=False):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    if verbose:
        for line in proc.stdout:
            line = line.decode('ascii')
            sys.stdout.write(line)
            if 'ERROR:' in line:
                raise Exception(line)
            sys.stdout.flush()

    out, err = proc.communicate()
