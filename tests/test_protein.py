from hypothesis import given
from minimal import minimal

from hypothesis_bio import protein


@given(protein())
def test_protein_type(seq):
    assert type(seq) == str

def test_smallest_example():
    assert minimal(protein()) == ""

def test_smallest_example_3_letter_abbrv():
    assert minimal(protein(single_letter_protein=False)) == ""

def test_smallest_non_empty_example():
    assert minimal(protein(min_size=1)) == "A"

def test_smallest_non_empty_example_3_letter_abbrv():
    seq = minimal(protein(single_letter_protein=False, min_size=1))
    assert len(seq) == 3
    assert seq == "Ala"

def test_2_mer():
    assert minimal(protein(min_size=2)) == "AA"

def test_2_mer_3_letter_abbrv():    
    seq = minimal(protein(single_letter_protein=False, min_size=2))
    assert len(seq) == 6
    assert seq == "AlaAla"

@given(protein(max_size=10))
def test_max_size(seq):
    assert len(seq) <= 10

def test_max_size_3_letter_abbrv():
    seq = minimal(protein(single_letter_protein=False, max_size=10))
    assert len(seq) <= 30
    assert len(seq) % 3 == 0
