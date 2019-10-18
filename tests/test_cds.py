from hypothesis import given
from minimal import minimal

from hypothesis_bio import cds


@given(cds())
def test_cds_type(seq):
    assert type(seq) == str


def test_smallest_example():
    assert minimal(cds()) == ""


def test_smallest_non_empty_example():
    assert minimal(cds(min_size=1)) == "ATG"


def test_2_mer():
    assert minimal(cds(min_size=2)) == "ATG"


@given(cds(max_size=10))
def test_max_size(seq):
    assert len(seq) <= 10
