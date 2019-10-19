import pytest

from hypothesis_bio import kmers

from .minimal import minimal


def test_smallest_example():
    assert minimal(kmers(seq="", k=0)) == ""


def test_smallest_non_empty_example_zero_k():
    assert minimal(kmers(seq="A", k=0)) == ""


def test_smallest_non_empty_example_non_zero_k():
    assert minimal(kmers(seq="A", k=1)) == "A"


def test_long_seq_example_non_zero_k():
    assert minimal(kmers(seq="ACGT", k=1)) == "A"


def test_long_seq_example_big_k():
    assert minimal(kmers(seq="ACGTACGT", k=4)) == "ACGT"


def test_exception():
    with pytest.raises(Exception):
        print(minimal(kmers(seq="A", k=5)))
