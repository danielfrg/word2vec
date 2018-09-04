#!/usr/bin/env bash

set -e
set -x

# Install miniconda
curl https://repo.continuum.io/miniconda/Miniconda3-4.5.11-Linux-x86_64.sh -L -k -o ~/miniconda.sh
bash ~/miniconda.sh -b -p $HOME/miniconda
export PATH=$HOME/miniconda/bin:$PATH

conda config --set always_yes yes --set changeps1 no
conda info -a

# Create "test" environment
conda create -n test python=$TRAVIS_PYTHON_VERSION
export PATH=$HOME/miniconda/envs/test/bin:$PATH

pip install -r requirements.txt
pip install -r ci/requirements-test.txt
