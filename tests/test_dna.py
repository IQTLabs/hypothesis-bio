from hypothesis import given

from hypothesis_bio import dna

from .minimal import minimal


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


def test_allow_gaps_smallest_example():
    seq = minimal(
        dna(min_size=1, allow_gaps=True, allow_ambiguous=False),
        lambda x: all(c not in ["A", "U", "C", "G"] for c in x),
    )
    assert seq == "-"


def test_allow_gaps_2_mer():
    seq = minimal(
        dna(min_size=2, allow_gaps=True, allow_ambiguous=False),
        lambda x: all(c not in ["A", "U", "C", "G"] for c in x),
    )
    assert seq == "--"


def test_allow_ambiguous_smallest_example():
    seq = minimal(
        dna(min_size=1, allow_ambiguous=True, allow_gaps=False, uppercase_only=True),
        lambda x: all(c not in ["A", "T", "C", "G"] for c in x),
    )
    assert seq == "B"


def test_allow_ambiguous_2_mer():
    seq = minimal(
        dna(min_size=2, allow_ambiguous=True, allow_gaps=False, uppercase_only=True),
        lambda x: all(c not in ["A", "T", "C", "G"] for c in x),
    )
    assert seq == "BB"


def test_allow_lowercase_smallest_example():
    seq = minimal(
        dna(min_size=1, uppercase_only=False, allow_gaps=False, allow_ambiguous=False),
        lambda x: all(c not in ["A", "T", "C", "G"] for c in x),
    )
    assert seq == "a"


def test_allow_lowercase_2_mer():
    seq = minimal(
        dna(min_size=2, uppercase_only=False, allow_gaps=False, allow_ambiguous=False),
        lambda x: all(c not in ["A", "T", "C", "G"] for c in x),
    )
    assert seq == "aa"
