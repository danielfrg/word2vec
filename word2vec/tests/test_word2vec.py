import os
import io
import sys
import numpy as np

import word2vec


input_ = os.path.expanduser("~/data/text8-1M")
output_phrases = os.path.expanduser("~/data/text-phrases.txt")
output_clusters = os.path.expanduser("~/data/text-clusters.txt")
output_bin = os.path.expanduser("~/data/vectors.bin")
output_txt = os.path.expanduser("~/data/vectors.txt")


def setup_module(module):
    word2vec.word2phrase(input_, output_phrases, verbose=False)
    word2vec.word2vec(input_, output_bin, size=10, binary=1, verbose=False)
    word2vec.word2vec(input_, output_txt, size=10, binary=0, verbose=False)
    word2vec.word2clusters(input_, output_clusters, 10, verbose=True)


def test_files_created_ok():
    # This are created on the setup_module
    assert os.path.exists(output_phrases)
    assert os.path.exists(output_clusters)
    assert os.path.exists(output_bin)
    assert os.path.exists(output_txt)


def test_load_bin():
    model = word2vec.load(output_bin)
    vocab = model.vocab
    vectors = model.vectors

    assert vectors.shape[0] == vocab.shape[0]
    assert vectors.shape[0] > 3000
    assert vectors.shape[1] == 10


def test_load_txt():
    model = word2vec.load(output_txt)
    vocab = model.vocab
    vectors = model.vectors

    assert vectors.shape[0] == vocab.shape[0]
    assert vectors.shape[0] > 3000
    assert vectors.shape[1] == 10


def test_distance():
    model = word2vec.load(output_txt)
    metrics = model.distance("the", "the", "the")
    assert len(metrics) == 3
    for item in metrics:
        # There should be 3 items per record
        assert len(item) == 3


def test_closest():
    model = word2vec.load(output_txt)
    indexes, metrics = model.closest(model["the"], n=30)
    assert indexes.shape == (30,)
    assert indexes.shape == metrics.shape

    py_response = model.generate_response(indexes, metrics).tolist()
    assert len(py_response) == 30
    assert len(py_response[0]) == 2


def test_similar():
    model = word2vec.load(output_bin)
    indexes, metrics = model.similar("the")
    assert indexes.shape == (10,)
    assert indexes.shape == metrics.shape

    py_response = model.generate_response(indexes, metrics).tolist()
    print(py_response)
    assert len(py_response) == 10
    assert len(py_response[0]) == 2


def test_analogy():
    model = word2vec.load(output_txt)
    indexes, metrics = model.analogy(pos=["the", "the"], neg=["the"], n=20)
    assert indexes.shape == (20,)
    assert indexes.shape == metrics.shape

    py_response = model.generate_response(indexes, metrics).tolist()
    assert len(py_response) == 20
    assert len(py_response[0]) == 2


def test_clusters():
    clusters = word2vec.load_clusters(output_clusters)
    assert clusters.vocab.shape == clusters.clusters.shape
    assert clusters.get_words_on_cluster(1).shape[0] > 10    # sanity check


def test_model_with_clusters():
    clusters = word2vec.load_clusters(output_clusters)
    model = word2vec.load(output_bin)
    assert clusters.vocab.shape == model.vocab.shape

    model.clusters = clusters
    indexes, metrics = model.analogy(pos=["the", "the"], neg=["the"], n=30)
    assert indexes.shape == (30,)
    assert indexes.shape == metrics.shape

    py_response = model.generate_response(indexes, metrics).tolist()
    assert len(py_response) == 30
    assert len(py_response[0]) == 3


def test_verbose():
    saved_stdout = sys.stdout

    try:
        sys.stdout = io.StringIO()

        word2vec.word2vec(input_, output_bin, size=10, binary=1, verbose=True)
        output = sys.stdout.getvalue()

        assert "b'" not in output
        assert "Starting training" in output
        assert "\\r" not in output
        assert "\r" in output

    finally:
        sys.stdout = saved_stdout
