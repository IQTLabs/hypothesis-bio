from hypothesis import given
from .minimal import minimal

from hypothesis_bio import dna


@given(dna())
def test_dna_type(seq):
    assert type(seq) == str


def test_smallest_example():
    assert minimal(dna()) == ""


def test_smallest_non_empty_example():
    assert minimal(dna(min_size=1)) == "A"


def test_2_mer():
    assert minimal(dna(min_size=2)) == "AA"


@given(dna(max_size=10))
def test_max_size(seq):
    assert len(seq) <= 10
