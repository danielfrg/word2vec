def test_import():
    import word2vec

    assert word2vec.__version__ is not None
    assert len(word2vec.__version__) > 0
