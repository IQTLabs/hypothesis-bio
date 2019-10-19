import pytest
from hypothesis import HealthCheck, given, settings
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
    with pytest.raises(ValueError):
        minimal(
            cds(
                min_size=3,
                max_size=3,
                include_start_codon=True,
                include_stop_codon=True,
            )
        )

    # but you can fit one
    assert (
        minimal(
            cds(
                min_size=3,
                max_size=3,
                include_start_codon=True,
                include_stop_codon=False,
            )
        )
        == "ATA"
    )
    assert (
        minimal(
            cds(
                min_size=3,
                max_size=3,
                include_start_codon=False,
                include_stop_codon=True,
            )
        )
        == "AGA"
    )

    # non mod 3 specific sizes won't work
    with pytest.raises(Unsatisfiable):

        @given(cds(min_size=7, max_size=7))
        @settings(suppress_health_check=HealthCheck.all())
        def inner(x):
            pass

        inner()

    with pytest.raises(Unsatisfiable):

        @given(cds(min_size=8, max_size=8))
        @settings(suppress_health_check=HealthCheck.all())
        def inner(x):
            pass

        inner()

    # if start and stop codons are included, there is no other codon in a 6-mer
    assert minimal(cds(min_size=6, max_size=6)) == "ATAAGA"


def test_allow_internal_stop_codons():
    assert (
        minimal(
            cds(
                min_size=3,
                allow_internal_stop_codons=False,
                include_start_codon=False,
                include_stop_codon=False,
                allow_ambiguous=False,
            ),
            lambda x: all(
                c not in ["AGA", "AGG", "TAA", "TAG", "TCA", "TGA", "TTA"] for c in x
            ),
        )
        == "AAA"
    )
