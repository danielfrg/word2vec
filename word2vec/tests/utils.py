# coding: utf-8
from nose.tools import eq_
from word2vec.utils import TopWords


def test_TopOrderedDict_1():
    ol = TopWords(10, distances=range(10), values=range(10, 20))

    eq_(ol.distances, range(10))
    eq_(ol.values, range(10, 20))

    # Insert: Middle
    ol.insert(6.5, 'a')
    d_ans = [0, 1, 2, 3, 4, 5, 6, 6.5, 7, 8]
    v_ans = [10, 11, 12, 13, 14, 15, 16, 'a', 17, 18]
    eq_(ol.distances, d_ans)
    eq_(ol.values, v_ans)

    # Distance to big, no change
    ol.insert(9, 'a')
    eq_(ol.distances, d_ans)
    eq_(ol.values, v_ans)

    # Insert: Middle
    ol.insert(2.5, 'b')
    d_ans = [0, 1, 2, 2.5, 3, 4, 5, 6, 6.5, 7]
    v_ans = [10, 11, 12, 'b', 13, 14, 15, 16, 'a', 17]
    eq_(ol.distances, d_ans)
    eq_(ol.values, v_ans)

    # Insert: new winner
    ol.insert(-1, 'z')
    d_ans = [-1, 0, 1, 2, 2.5, 3, 4, 5, 6, 6.5]
    v_ans = ['z', 10, 11, 12, 'b', 13, 14, 15, 16, 'a']
    eq_(ol.distances, d_ans)
    eq_(ol.values, v_ans)

    # If distance is the same put it below existing value
    ol.insert(0, 'g')
    d_ans = [-1, 0, 0, 1, 2, 2.5, 3, 4, 5, 6]
    v_ans = ['z', 10, 'g', 11, 12, 'b', 13, 14, 15, 16]
    eq_(ol.distances, d_ans)
    eq_(ol.values, v_ans)

    # Distance to big, no change
    ol.insert(6, 'y')
    eq_(ol.distances, d_ans)
    eq_(ol.values, v_ans)

    # Insert: last posision
    ol.insert(5.4, 'y')
    d_ans = [-1, 0, 0, 1, 2, 2.5, 3, 4, 5, 5.4]
    v_ans = ['z', 10, 'g', 11, 12, 'b', 13, 14, 15, 'y']
    eq_(ol.distances, d_ans)
    eq_(ol.values, v_ans)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vs', '--nologcapture'], exit=False)
