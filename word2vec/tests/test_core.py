import io
import os
import sys

import pytest

import word2vec


this_dir = os.path.abspath(os.path.dirname(__file__))
default_data_dir = os.path.abspath(os.path.join(this_dir, "..", "..", "data"))
data_dir = os.environ.get("WORD2VEC_TEST_DATA", default_data_dir)
input_text = os.path.join(data_dir, "text8-small")
output_phrases = os.path.join(data_dir, "test-output-text-phrases.txt")
output_clusters = os.path.join(data_dir, "test-output-text-clusters.txt")
output_txt = os.path.join(data_dir, "test-output-vectors.txt")
output_bin = os.path.join(data_dir, "test-output-vectors.bin")


@pytest.mark.data
def test_run_word2vec():
    word2vec.word2vec(input_text, output_txt)
    assert os.path.exists(output_txt)


@pytest.mark.data
def test_run_word2vec_bin():
    word2vec.word2vec(input_text, output_bin, binary=1)
    assert os.path.exists(output_bin)


@pytest.mark.data
@pytest.mark.xfail(sys.platform == "darwin", reason="Failing on OS X")
@pytest.mark.xfail(
    os.environ.get("CI", None) is not None,
    reason="Failing on Github Actions: Aborted (core dumped)",
)
def test_run_word2phrase():
    word2vec.word2phrase(input_text, output_phrases)
    assert os.path.exists(output_phrases)


@pytest.mark.data
def test_run_word2clusters():
    word2vec.word2clusters(input_text, output_clusters, 10)
    assert os.path.exists(output_clusters)


@pytest.mark.data
def test_load_bin():
    model = word2vec.load(output_txt)
    vocab = model.vocab
    vectors = model.vectors

    assert vectors.shape[0] == vocab.shape[0]
    assert vectors.shape[0] > 500
    assert vectors.shape[1] == 100


@pytest.mark.data
def test_load_txt():
    model = word2vec.load(output_txt)
    vocab = model.vocab
    vectors = model.vectors

    assert vectors.shape[0] == vocab.shape[0]
    assert vectors.shape[0] > 500
    assert vectors.shape[1] == 100


@pytest.mark.data
def test_distance():
    model = word2vec.load(output_txt)
    metrics = model.distance("the", "the", "the")
    assert len(metrics) == 3
    for item in metrics:
        # There should be 3 items per record
        assert len(item) == 3


@pytest.mark.data
def test_closest():
    model = word2vec.load(output_txt)
    indexes, metrics = model.closest(model["the"], n=30)
    assert indexes.shape == (30,)
    assert indexes.shape == metrics.shape

    py_response = model.generate_response(indexes, metrics).tolist()
    assert len(py_response) == 30
    assert len(py_response[0]) == 2


@pytest.mark.data
def test_similar():
    model = word2vec.load(output_txt)
    indexes, metrics = model.similar("the")
    assert indexes.shape == (10,)
    assert indexes.shape == metrics.shape

    py_response = model.generate_response(indexes, metrics).tolist()
    assert len(py_response) == 10
    assert len(py_response[0]) == 2


@pytest.mark.data
def test_analogy():
    model = word2vec.load(output_txt)
    indexes, metrics = model.analogy(pos=["the", "the"], neg=["the"], n=20)
    assert indexes.shape == (20,)
    assert indexes.shape == metrics.shape

    py_response = model.generate_response(indexes, metrics).tolist()
    assert len(py_response) == 20
    assert len(py_response[0]) == 2


@pytest.mark.data
def test_clusters():
    clusters = word2vec.load_clusters(output_clusters)
    assert clusters.vocab.shape == clusters.clusters.shape
    assert clusters.get_words_on_cluster(1).shape[0] > 10  # sanity check


@pytest.mark.data
def test_model_with_clusters():
    clusters = word2vec.load_clusters(output_clusters)
    model = word2vec.load(output_txt)
    assert clusters.vocab.shape == model.vocab.shape

    model.clusters = clusters
    indexes, metrics = model.analogy(pos=["the", "the"], neg=["the"], n=30)
    assert indexes.shape == (30,)
    assert indexes.shape == metrics.shape

    py_response = model.generate_response(indexes, metrics).tolist()
    assert len(py_response) == 30
    assert len(py_response[0]) == 3


@pytest.mark.data
def test_verbose():
    saved_stdout = sys.stdout

    try:
        sys.stdout = io.StringIO()

        word2vec.word2vec(input_text, output_txt, size=10, verbose=True)
        output = sys.stdout.getvalue()

        assert "b'" not in output
        assert "Starting training" in output
        assert "\\r" not in output
        assert "\r" not in output

    finally:
        sys.stdout = saved_stdout
