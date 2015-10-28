"""
To upload a new version:
1. make clean
2. git tag a new version: git tag v1.x.x
3. python setup.py sdist
4. python setup.py sdist register upload
"""

from distutils.core import setup
from setuptools import find_packages

import os
import sys
import subprocess

import versioneer

SOURCES_DIR = 'word2vec-c'
BIN_DIR = 'bin'
if not os.path.exists(BIN_DIR):
    os.makedirs(BIN_DIR)

def compile_c(source, target):
    CC = 'gcc'
    CFLAGS = ('-lm -pthread -O3 -Wall -march=native -funroll-loops '
              '-Wno-unused-result')
    if sys.platform == 'darwin':
        CFLAGS += ' -I/usr/include/malloc'

    source_path = os.path.join(SOURCES_DIR, source)
    target_path = os.path.join(BIN_DIR, target)
    command = [CC, source_path, '-o', target_path]
    command.extend(CFLAGS.split(' '))
    print(' '.join(command))
    return_code = subprocess.call(command)

    if return_code > 0:
        exit(return_code)

compile_c('word2vec.c', 'word2vec')
compile_c('word2phrase.c', 'word2phrase')
compile_c('distance.c', 'word2vec-distance')
compile_c('word-analogy.c', 'word2vec-word-analogy')
compile_c('compute-accuracy.c', 'word2vec-compute-accuracy')
compile_c('word2vec-sentence2vec.c', 'word2vec-doc2vec')

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='word2vec',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Daniel Rodriguez',
    author_email='df.rodriguez143@gmail.com',
    url='https://github.com/danielfrg/word2vec',
    description='Wrapper for Google word2vec',
    license='Apache License Version 2.0, January 2004',
    packages=find_packages(),
    data_files=[('bin', ['bin/word2vec', 'bin/word2phrase',
                         'bin/word2vec-distance', 'bin/word2vec-word-analogy',
                         'bin/word2vec-compute-accuracy',
                         'bin/word2vec-doc2vec'])],
    install_requires=required
)
