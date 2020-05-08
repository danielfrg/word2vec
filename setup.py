import os
import subprocess
import sys

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install


setup_dir = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    filepath = os.path.join(setup_dir, filename)
    with open(filepath) as file:
        return file.read()


class InstallCmd(install):
    def run(self):
        print("Running custom Install command")
        compile_all()
        super(InstallCmd, self).run()


class DevelopCmd(develop):
    def run(self):
        print("Running custom Develop command")
        compile_all()
        super(DevelopCmd, self).run()


def compile_all():
    if sys.platform == "win32":
        compile_c("win32/word2vec.c", "word2vec.exe")
        compile_c("win32/word2phrase.c", "word2phrase.exe")
        compile_c("win32/distance.c", "word2vec-distance.exe")
        compile_c("win32/word-analogy.c", "word2vec-word-analogy.exe")
        compile_c("win32/compute-accuracy.c", "word2vec-compute-accuracy.exe")
    else:
        compile_c("word2vec.c", "word2vec")
        compile_c("word2phrase.c", "word2phrase")
        compile_c("distance.c", "word2vec-distance")
        compile_c("word-analogy.c", "word2vec-word-analogy")
        compile_c("compute-accuracy.c", "word2vec-compute-accuracy")
        compile_c("word2vec-sentence2vec.c", "word2vec-doc2vec")


def compile_c(source, target):
    this_dir = os.path.abspath(os.path.dirname(__file__))
    c_source = os.path.join(this_dir, "word2vec", "includes")

    if sys.platform == "win32":
        target_dir = "Scripts"
    else:
        target_dir = "bin"

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    CC = "gcc"

    DEFAULT_CFLAGS = (
        "-lm -pthread -Ofast -Wall -march=native -funroll-loops -Wno-unused-result"
    )

    if sys.platform == "darwin":
        DEFAULT_CFLAGS += " -I/usr/include/malloc"

    if sys.platform == "win32":
        DEFAULT_CFLAGS = "-O2 -Wall -funroll-loops"

    CFLAGS = os.environ.get("WORD2VEC_CFLAGS", DEFAULT_CFLAGS)

    source = os.path.join(c_source, source)
    target = os.path.join(target_dir, target)
    command = [CC, source, "-o", target]
    command.extend(CFLAGS.split(" "))

    print("Compiling:", " ".join(command))
    return_code = subprocess.call(command)

    if return_code > 0:
        exit(return_code)


# Create the files for the data_files
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
    use_scm_version=True,
    packages=find_packages(),
    # package_dir={"": "src"},
    zip_safe=False,
    include_package_data=True,
    package_data={"word2vec": ["includes/**/*.c"]},
    data_files=data_files,
    cmdclass={"install": InstallCmd, "develop": DevelopCmd},
    # entry_points = {},
    options={"bdist_wheel": {"universal": "1"}},
    python_requires=">=3.6",
    setup_requires=["setuptools_scm"],
    install_requires=read_file("requirements-package.txt").splitlines(),
    extras_require={"dev": read_file("requirements.txt").splitlines()},
    description="Wrapper for Google word2vec",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    license="Apache License, Version 2.0",
    maintainer="Daniel Rodriguez",
    maintainer_email="daniel@danielfrg.com",
    url="https://github.com/danielfrg/word2vec",
    keywords=["NLP", "word2vec"],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
