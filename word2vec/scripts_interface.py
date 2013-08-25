# coding: utf-8
import subprocess


def word2vec(train, output, size=100, window=5, sample=0, hs=1, negative=0, threads=4,
             min_count=5, alpha=0.025, debug=2, binary=0, cbow=0,
             save_vocab=None, read_vocab=None):
    process = ['word2vec']
    args = ['-train', '-output', '-size', '-window', '-sample', '-hs', '-negative', '-threads',
            '-min-count', '-alpha', '-debug', '-binary', '-cbow']
    values = [train, output, size, window, sample, hs, negative, threads,
              min_count, alpha, debug, binary, cbow]
    for arg, value in zip(args, values):
        process.append(arg)
        process.append(str(value))
    if save_vocab is not None:
        process.append('-save-vocab')
        process.append(str(save_vocab))
    if read_vocab is not None:
        process.append('-read-vocab')
        process.append(str(read_vocab))
    subprocess.call(process)


def word2clusters(train, output, classes, size=100, window=5, sample=0, hs=1, negative=0, threads=4,
                  min_count=5, alpha=0.025, debug=2, binary=0, cbow=0,
                  save_vocab=None, read_vocab=None):
    process = ['word2vec']
    args = ['-train', '-output', '-size', '-window', '-sample', '-hs', '-negative', '-threads',
            '-min-count', '-alpha', '-classes', '-debug', '-binary', '-cbow']
    values = [train, output, size, window, sample, hs, negative, threads,
              min_count, alpha, classes, debug, binary, cbow]
    for arg, value in zip(args, values):
        process.append(arg)
        process.append(str(value))
    if save_vocab is not None:
        process.append('-save-vocab')
        process.append(str(save_vocab))
    if read_vocab is not None:
        process.append('-read-vocab')
        process.append(str(read_vocab))
    subprocess.call(process)


def word2phase(train, output, min_count=5, threshold=100, debug=2):
    process = ['word2phrase']
    args = ['-train', '-output', '-min-count', '-threshold', '-debug']
    values = [train, output, min_count, threshold, debug]
    for arg, value in zip(args, values):
        process.append(arg)
        process.append(str(value))
    subprocess.call(process)

if __name__ == '__main__':
    word2vec_classes('../data/text8', 'text8-classes.txt', 100)
