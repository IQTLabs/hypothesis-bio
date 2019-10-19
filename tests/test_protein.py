from hypothesis import given

from hypothesis_bio import protein

from .minimal import minimal


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


def test_allow_ambiguous():
    seq = minimal(
        protein(
            single_letter_protein=True,
            allow_ambiguous=True,
            allow_extended=False,
            min_size=1,
            max_size=1,
        ),
        lambda x: x not in norm_AA.keys(),
    )
    assert seq == "X"


def test_allow_ambiguous_3_letter_abbrv():
    seq = minimal(
        protein(
            single_letter_protein=False,
            allow_ambiguous=True,
            allow_extended=False,
            min_size=1,
            max_size=1,
        ),
        lambda x: x not in norm_AA.values(),
    )
    assert seq == "Xaa"


def test_allow_extended():
    seq = minimal(
        protein(
            single_letter_protein=True,
            allow_ambiguous=False,
            allow_extended=True,
            min_size=1,
            max_size=1,
        ),
        lambda x: x not in norm_AA.keys(),
    )
    assert seq == "B"


def test_allow_extended_3_letter_abbrv():
    seq = minimal(
        protein(
            single_letter_protein=False,
            allow_ambiguous=False,
            allow_extended=True,
            min_size=1,
            max_size=1,
        ),
        lambda x: x not in norm_AA.values(),
    )
    assert seq == "Asx"


def test_uppercase_only():
    seq = minimal(protein(single_letter_protein=True, uppercase_only=True, min_size=1))
    assert seq == "A"


def test_uppercase_only_3_letter_abbrv():
    seq = minimal(protein(single_letter_protein=False, uppercase_only=True, min_size=1))
    assert seq == "ALA"


def test_not_uppercase_only():
    seq = minimal(
        protein(single_letter_protein=True, uppercase_only=False, min_size=1),
        lambda x: all(not c.isupper() for c in x),
    )
    assert seq == "a"


def test_not_uppercase_only_3_letter_abbrv():
    seq = minimal(
        protein(single_letter_protein=False, uppercase_only=False, min_size=1),
        # lambda x: all(not c.isupper() for c in x)
    )
    assert seq == "Ala"


norm_AA = {
    "A": "Ala",
    "C": "Cys",
    "D": "Asp",
    "E": "Glu",
    "F": "Phe",
    "G": "Gly",
    "H": "His",
    "I": "Ile",
    "K": "Lys",
    "L": "Leu",
    "M": "Met",
    "N": "Asn",
    "P": "Pro",
    "Q": "Gln",
    "R": "Arg",
    "S": "Ser",
    "T": "Thr",
    "V": "Val",
    "W": "Trp",
    "Y": "Tyr",
}
