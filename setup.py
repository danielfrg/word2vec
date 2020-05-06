import os
import subprocess
import sys

from setuptools import dist, find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install

setup_dir = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    this_dir = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(this_dir, filename)
    with open(filepath) as file:
        return file.read()


def parse_git(root, **kwargs):
    """
    Parse function for setuptools_scm
    """
    from setuptools_scm.git import parse

    kwargs["describe_command"] = "git describe --dirty --tags --long"
    return parse(root, **kwargs)


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
    this_dir = os.path.abspath(os.path.dirname(__file__))
    c_source = os.path.join(this_dir, "word2vec", "include")

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
    packages=find_packages() + ["word2vec.tests"],
    zip_safe=False,
    include_package_data=True,
    package_data={"word2vec": ["includes/**/*.c"]},
    data_files=data_files,
    cmdclass={"install": InstallCmd, "develop": DevelopCmd},
    # entry_points = {},
    use_scm_version={
        "root": setup_dir,
        "parse": parse_git,
        "write_to": os.path.join("word2vec/_generated_version.py"),
    },
    test_suite="word2vec/tests",
    setup_requires=["setuptools_scm"],
    install_requires=read_file("requirements.package.txt").splitlines(),
    tests_require=["pytest",],
    python_requires=">=3.5",
    description="Wrapper for Google word2vec",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    license="Apache License, Version 2.0",
    maintainer="Daniel Rodriguez",
    maintainer_email="daniel@danielfrg.com",
    url="https://github.com/danielfrg/word2vec",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords=["NLP", "word2vec"],
)
