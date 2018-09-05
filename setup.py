from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install as _install
from Cython.Build import cythonize

import os
import sys
import subprocess

import versioneer

THIS_DIR = os.path.abspath(os.path.dirname(__file__))


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
    filepath = os.path.join(THIS_DIR, filename)
    with open(filepath) as file:
        return file.read()


REQUIREMENTS = read_file("requirements.txt").splitlines()

data_files = []
if sys.platform == "win32":
    out_data_files = [
        "Scripts/word2vec.exe",
        "Scripts/word2phrase.exe",
        "Scripts/word2vec-distance.exe",
        "Scripts/word2vec-word-analogy.exe",
        "Scripts/word2vec-compute-accuracy.exe",
    ]
    data_files = [("Scripts", out_data_files)]
else:
    out_data_files = [
        "bin/word2vec",
        "bin/word2phrase",
        "bin/word2vec-distance",
        "bin/word2vec-word-analogy",
        "bin/word2vec-compute-accuracy",
        "bin/word2vec-doc2vec",
    ]
    data_files = [("bin", out_data_files)]

setup(
    name="word2vec",
    version=versioneer.get_version(),
    cmdclass=cmdclass,
    ext_modules=cythonize("word2vec/word2vec_noop.pyx"),
    author="Daniel Rodriguez",
    author_email="df.rodriguez143@gmail.com",
    url="https://github.com/danielfrg/word2vec",
    description="Wrapper for Google word2vec",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    license="Apache License Version 2.0, January 2004",
    packages=find_packages(),
    data_files=data_files,
    python_requires=">=3.0,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
    install_requires=REQUIREMENTS,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
