import pytest
from hypothesis import given
from hypothesis.errors import InvalidArgument, Unsatisfiable

from hypothesis_bio import cds

from .minimal import minimal


@given(cds())
def test_cds_type(seq):
    assert type(seq) == str


def test_smallest_example():
    assert minimal(cds(include_start_codon=False, include_stop_codon=False)) == ""


def test_smallest_example_with_start_codon():
    assert minimal(cds(include_start_codon=True, include_stop_codon=False)) == "ATA"


def test_smallest_example_with_stop_codon():
    assert minimal(cds(include_start_codon=False, include_stop_codon=True)) == "AGA"


def test_smallest_non_empty_coding_region():
    assert minimal(cds(min_size=1)) == "ATAAGA"


def test_total_size_mer():
    assert minimal(cds(min_size=4)) == "ATAAGA"


def test_size_with_codon():
    assert minimal(cds(min_size=7)) == "ATAAAAAGA"


@given(cds(max_size=10))
def test_max_size(seq):
    assert len(seq) <= 10


@given(cds())
def test_length_modulo_3(seq):
    assert len(seq) % 3 == 0


def test_max_size_less_than_min_size():
    with pytest.raises(InvalidArgument):
        minimal(cds(min_size=10, max_size=9))


def test_min_size_equal_to_max_size():

    # you can't fit two codons in 3 bases
    with pytest.raises(Unsatisfiable):
        minimal(
            cds(
                min_size=3,
                max_size=3,
                include_start_codon=True,
                include_stop_codon=True,
            )
        )

    # or 2 for that matter
    with pytest.raises(Unsatisfiable):
        minimal(
            cds(
                min_size=2,
                max_size=2,
                include_start_codon=True,
                include_stop_codon=True,
            )
        )

    # non mod 3 specific sizes won't work
    with pytest.raises(Unsatisfiable):
        minimal(cds(min_size=4, max_size=4))
    with pytest.raises(Unsatisfiable):
        minimal(cds(min_size=7, max_size=7))

    # if start and stop codons are included, there is no other codon in a 6-mer
    assert minimal(cds(min_size=6, max_size=6)) == "ATAAGA"
