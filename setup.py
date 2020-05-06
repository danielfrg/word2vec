import os
import sys

import versioneer
from setuptools import find_packages, setup

import subprocess
from setuptools import dist
from setuptools import setup
from setuptools import find_packages

# First install Cython and six becuase we use then on setup
from setuptools.command.install import install as _install
dist.Distribution().fetch_build_eggs(['Cython', 'six'])

try:
    from Cython.Build import cythonize
except ImportError:
    # create closure for deferred import
    def cythonize (*args, ** kwargs ):
        from Cython.Build import cythonize
        return cythonize(*args, ** kwargs)


class install(_install):

    def run(self):
        self.C_SOURCE = os.path.join(THIS_DIR, "word2vec", "src")

        self.TARGET_DIR = "bin"
        if sys.platform == "win32":
            self.TARGET_DIR = "Scripts"

        if not os.path.exists(self.TARGET_DIR):
            os.makedirs(self.TARGET_DIR)

        if sys.platform == "win32":
            self.compile_c("win32/word2vec.c", "word2vec.exe")
            self.compile_c("win32/word2phrase.c", "word2phrase.exe")
            self.compile_c("win32/distance.c", "word2vec-distance.exe")
            self.compile_c("win32/word-analogy.c", "word2vec-word-analogy.exe")
            self.compile_c("win32/compute-accuracy.c", "word2vec-compute-accuracy.exe")
        else:
            self.compile_c("word2vec.c", "word2vec")
            self.compile_c("word2phrase.c", "word2phrase")
            self.compile_c("distance.c", "word2vec-distance")
            self.compile_c("word-analogy.c", "word2vec-word-analogy")
            self.compile_c("compute-accuracy.c", "word2vec-compute-accuracy")
            self.compile_c("word2vec-sentence2vec.c", "word2vec-doc2vec")

        _install.run(self)

    def compile_c(self, source, target):
        CC = "gcc"

        DEFAULT_CFLAGS = "-lm -pthread -O3 -Wall -march=native -funroll-loops"
        DEFAULT_CFLAGS += " -Wno-unused-result"
        if sys.platform == "darwin":
            DEFAULT_CFLAGS += " -I/usr/include/malloc"
        if sys.platform == "win32":
            DEFAULT_CFLAGS = "-O2 -Wall -funroll-loops"
        CFLAGS = os.environ.get("W2V_CFLAGS", DEFAULT_CFLAGS)

        source_path = os.path.join(self.C_SOURCE, source)
        target_path = os.path.join(self.TARGET_DIR, target)
        command = [CC, source_path, "-o", target_path]
        command.extend(CFLAGS.split(" "))
        print("Compilation command:", " ".join(command))
        return_code = subprocess.call(command)

        if return_code > 0:
            exit(return_code)


cmdclass = versioneer.get_cmdclass()
cmdclass.update({"install": install})


def read_file(filename):
    this_dir = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(this_dir, filename)
    with open(filepath) as file:
        return file.read()


data_files = []
if sys.platform == "win32":
    files = [
        "Scripts/word2vec.exe",
        "Scripts/word2phrase.exe",
        "Scripts/word2vec-distance.exe",
        "Scripts/word2vec-word-analogy.exe",
        "Scripts/word2vec-compute-accuracy.exe",
    ]
    data_files = [("Scripts", files)]
else:
    files = [
        "bin/word2vec",
        "bin/word2phrase",
        "bin/word2vec-distance",
        "bin/word2vec-word-analogy",
        "bin/word2vec-compute-accuracy",
        "bin/word2vec-doc2vec",
    ]
    data_files = [("bin", files)]


setup(
    name="word2vec",
    version=versioneer.get_version(),
    description="Wrapper for Google word2vec",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    author="Daniel Rodriguez",
    author_email="daniel@danielfrg.com",
    url="https://github.com/danielfrg/word2vec",
    license="Apache License Version 2.0",
    python_requires=">=3.0,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*",
    install_requires=read_file("requirements.package.txt").splitlines(),
    keywords=["NLP", "word2vec", "cython"],
    packages=find_packages(),
    include_package_data=True,
    data_files=data_files,
    zip_safe=False,
    cmdclass=versioneer.get_cmdclass(),
    entry_points = {},
)
