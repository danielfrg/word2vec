import os
import subprocess
from distutils.core import setup

'''
To update to a new version:
1. change version
2. python setup.py sdist bdist_wininst upload
'''

DESCRIPTION = 'Google word2vec python wrapper'

directory = 'bin'
if not os.path.exists(directory):
    os.makedirs(directory)

subprocess.call(['make', '-C', 'word2vec-c'])

setup(
    name='word2vec',
    version='0.5',
    maintainer='Daniel Rodriguez',
    maintainer_email='df.rodriguez143@gmail.com',
    url='https://github.com/danielfrg/word2vec',
    packages=['word2vec'],
    description=DESCRIPTION,
    license='Apache License Version 2.0, January 2004',
    data_files=[('bin', ['bin/word2vec', 'bin/word2phrase', 'bin/w2v-distance',
                         'bin/w2v-word-analogy', 'bin/w2v-compute-accuracy'])],
    install_requires=[
        'numpy>=1.7.1'
    ],
)
