from hypothesis import given
from .minimal import minimal

from hypothesis_bio import protein

from unittest.mock import Mock

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


# unwraps a function wrapped with the @composite decorator - this is horrible, should be refactored
def get_unwrapped_function_from_composite_decorator(function):
    accept_function = function.__wrapped__
    composite_strategy = accept_function()
    original_function = composite_strategy.definition
    return original_function


def test_protein__ACD_is_drawn_returns_AlaCysAsp():
    # setup
    draw_mock = Mock(return_value="ACD")
    original_protein = get_unwrapped_function_from_composite_decorator(protein)

    # call
    actual = original_protein(draw_mock, single_letter_protein=False) # the others params do not matter as "ACD" is always drawn regardless of what is passed

    # assert
    expected = "AlaCysAsp"
    assert actual == expected


def test_protein__acd_is_drawn_returns_AlaCysAsp():
    draw_mock = Mock(return_value="acd")
    original_protein = get_unwrapped_function_from_composite_decorator(protein)

    actual = original_protein(draw_mock, single_letter_protein=False)

    expected = "AlaCysAsp"
    assert actual == expected  # fails because utilities.protein_1to3 does not contain lowercase entries