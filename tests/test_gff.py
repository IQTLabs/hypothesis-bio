from hypothesis import given

from hypothesis_bio import dna, gff, gff_entry

from .minimal import minimal

@given(gff_entry())
def test_return_type(seq):
    assert type(seq) == str
