"""
To upload a new version:
1. make clean
2. git tag a new version: git tag v1.x.x
3. python setup.py sdist
4. python setup.py sdist register upload

Note in binary files (`data_files`) from `setup()` below:

- When you do `python setup.py install` it will place the
binary files (`word2vec`, `word2phrase`, ...) in: `$(pwd)/bin`
So you have to export that to the `$PATH`
- When you do `pip install word2vec` it will place them in the correct
`{{ environtment }}/bin` directory so users dont need to do that.
"""

from setuptools import setup
from setuptools import find_packages
from  setuptools.command.install import install as _install
from Cython.Build import cythonize

import os
import sys
import subprocess

import versioneer


class install(_install):
    def run(self):
        self.C_SOURCE = os.path.join('word2vec', 'c')
        self.BIN_DIR = 'bin'
        if not os.path.exists(self.BIN_DIR):
            os.makedirs(self.BIN_DIR)

        self.compile_c('word2vec.c', 'word2vec')
        self.compile_c('word2phrase.c', 'word2phrase')
        self.compile_c('distance.c', 'word2vec-distance')
        self.compile_c('word-analogy.c', 'word2vec-word-analogy')
        self.compile_c('compute-accuracy.c', 'word2vec-compute-accuracy')
        self.compile_c('word2vec-sentence2vec.c', 'word2vec-doc2vec')

        _install.run(self)

    def compile_c(self, source, target):
        CC = 'gcc'

        DEFAULT_CFLAGS = ('-lm -pthread -O3 -Wall -march=native -funroll-loops '
                  '-Wno-unused-result')
        if sys.platform == 'darwin':
            DEFAULT_CFLAGS += ' -I/usr/include/malloc'
        CFLAGS = os.environ.get('CFLAGS', DEFAULT_CFLAGS)

        source_path = os.path.join(self.C_SOURCE, source)
        target_path = os.path.join(self.BIN_DIR, target)
        command = [CC, source_path, '-o', target_path]
        command.extend(CFLAGS.split(' '))
        print('Compilation command:', ' '.join(command))
        return_code = subprocess.call(command)

        if return_code > 0:
            exit(return_code)

with open('requirements.txt') as f:
    required = f.read().splitlines()

cmdclass=versioneer.get_cmdclass()
cmdclass.update({'install': install})

setup(
    name='word2vec',
    version=versioneer.get_version(),
    cmdclass=cmdclass,
    ext_modules=cythonize("word2vec/noop.pyx"),
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
