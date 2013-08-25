# encoding: utf-8
import subprocess
from distutils.core import setup
from distutils.extension import Extension
DESCRIPTION = 'Google word2vec python wrapper'

ext_modules = None
word2vec = Extension('word2vec',
                     sources=['word2vec-src/word2vec.c'],
                     extra_link_args=['-lm', '-pthread', '-O2', '-Wall', '-funroll-loops'])
ext_modules = [word2vec]
ext_modules = []

subprocess.call(['make', '-C', 'word2vec-src'])

setup(
    name='word2vec',
    version='0.0.1',
    maintainer='Daniel Rodriguez',
    maintainer_email='df.rodriguez143@gmail.com',
    ext_modules=ext_modules,
    description=DESCRIPTION,
    license='see LICENCE.txt',
    data_files=[('bin', ['bin/word2vec', 'bin/word2phrase', 'bin/w2v-distance',
                         'bin/w2v-word-analogy', 'bin/w2v-compute-accuracy'])]
)
