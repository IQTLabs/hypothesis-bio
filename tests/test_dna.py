from hypothesis import given
from hypothesis_bio import dna


@given(dna())
def test_dna_type(seq):
    assert type(seq) == str
