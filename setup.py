# encoding: utf-8
import os
import subprocess
from distutils.core import setup

DESCRIPTION = 'Google word2vec python wrapper'

directory = 'bin'
if not os.path.exists(directory):
    os.makedirs(directory)

subprocess.call(['make', '-C', 'word2vec-src'])

setup(
    name='word2vec',
    version='0.0.1',
    maintainer='Daniel Rodriguez',
    maintainer_email='df.rodriguez143@gmail.com',
    url='https://github.com/danielfrg/word2vec',
    packages=['word2vec', 'word2vec.tests'],
    description=DESCRIPTION,
    license='Apache License Version 2.0, January 2004',
    data_files=[('bin', ['bin/word2vec', 'bin/word2phrase', 'bin/w2v-distance',
                         'bin/w2v-word-analogy', 'bin/w2v-compute-accuracy'])],
    install_requires=[
        'numpy==1.7.1',
        'scipy==0.12.0'
    ],
)
