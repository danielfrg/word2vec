import os
import sys
import subprocess
from distutils.core import setup

'''
To update to a new version:
1. change version
2. python setup.py sdist upload
'''

DESCRIPTION = 'Google word2vec python wrapper'

SOURCES_DIR = 'word2vec-c'
BIN_DIR = 'bin'
if not os.path.exists(BIN_DIR):
    os.makedirs(BIN_DIR)

def compile(source, target):
    CC = 'gcc'
    CFLAGS = '-lm -pthread -O3 -Wall -march=native -funroll-loops -Wno-unused-result'
    if sys.platform == 'darwin':
        CFLAGS += ' -I/usr/include/malloc'

    source_path = os.path.join(SOURCES_DIR, source)
    target_path = os.path.join(BIN_DIR, target)
    command = [CC, source_path, '-o', target_path]
    command.extend(CFLAGS.split(' '))
    print ' '.join(command)
    return_code = subprocess.call(command)

    if return_code > 0:
        exit(return_code)

compile('word2vec.c', 'word2vec')
compile('word2phrase.c', 'word2phrase')
compile('distance.c', 'w2v-distance')
compile('word-analogy.c', 'w2v-word-analogy')
compile('compute-accuracy.c', 'w2v-compute-accuracy')

setup(
    name='word2vec',
    version='0.7.1',
    maintainer='Daniel Rodriguez',
    maintainer_email='df.rodriguez143@gmail.com',
    url='https://github.com/danielfrg/word2vec',
    packages=['word2vec'],
    description=DESCRIPTION,
    license='Apache License Version 2.0, January 2004',
    data_files=[('bin', ['bin/word2vec', 'bin/word2phrase', 'bin/w2v-distance',
                         'bin/w2v-word-analogy', 'bin/w2v-compute-accuracy'])],
    install_requires=[
        'numpy>=1.9.2'
    ],
)
