from hypothesis import given
from minimal import minimal

from hypothesis_bio import cds


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
def test_length(seq):
    assert len(seq) % 3 == 0
