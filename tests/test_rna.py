from hypothesis import given

from hypothesis_bio import rna

from .minimal import minimal


@given(rna())
def test_rna_type(seq):
    assert type(seq) == str


def test_smallest_example():
    assert minimal(rna()) == ""


def test_smallest_non_empty_example():
    assert minimal(rna(min_size=1)) == "A"


def test_2_mer():
    assert minimal(rna(min_size=2)) == "AA"


@given(rna(max_size=10))
def test_max_size(seq):
    assert len(seq) <= 10
