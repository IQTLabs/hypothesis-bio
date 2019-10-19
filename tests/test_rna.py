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


def test_allow_gaps_smallest_example():
    seq = minimal(
        rna(min_size=1, allow_gaps=True),
        lambda x: all(c not in ["A", "U", "C", "G"] for c in x),
    )
    assert seq == "-"


def test_allow_gaps_2_mer():
    seq = minimal(
        rna(min_size=2, allow_gaps=True),
        lambda x: all(c not in ["A", "U", "C", "G"] for c in x),
    )
    assert seq == "--"


def test_allow_lowercase_smallest_example():
    seq = minimal(
        rna(min_size=1, allow_lowercase=True),
        lambda x: all(c not in ["A", "U", "C", "G"] for c in x),
    )
    assert seq == "a"


def test_allow_lowercase_2_mer():
    seq = minimal(
        rna(min_size=2, allow_lowercase=True),
        lambda x: all(c not in ["A", "U", "C", "G"] for c in x),
    )
    assert seq == "aa"


def test_allow_ambiguous_smallest_example():
    seq = minimal(
        rna(min_size=1, allow_ambiguous=True),
        lambda x: all(c not in ["A", "U", "C", "G"] for c in x),
    )
    assert seq == "B"


def test_allow_ambiguous_2_mer():
    seq = minimal(
        rna(min_size=2, allow_ambiguous=True),
        lambda x: all(c not in ["A", "U", "C", "G"] for c in x),
    )
    assert seq == "BB"
