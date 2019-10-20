from .minimal import minimal

from hypothesis_bio.pdb import generate_date, generate_idcode, generate_token, generate_lstring, generate_real, generate_header, generate_specification, generate_obslte, generate_title


def test_generate_date():
    assert minimal(generate_date()) == "01-JAN-00"


def test_generate_idcode():
    assert minimal(generate_idcode()) == "0000"


def test_generate_token_smallest():
    assert minimal(generate_token()) == "0: "


def test_generate_lstring():
    assert minimal(generate_lstring()) == "0"


def test_generate_real():
    assert minimal(generate_real()) == "F0.0"


def test_generate_header():
    assert minimal(generate_header()) == "HEADER" + " " * 43 + "01-JAN-00   0000"


def test_generate_specification():
    assert minimal(generate_specification()) == "0: 0"


def test_generate_obslte():
    assert minimal(generate_obslte()) == "OBSLTE" + " " * 4 + "01-JAN-00 0000      0000"


def test_generate_obslte_continuation():
    assert minimal(generate_obslte(continuation_number=2)) == "OBSLTE  2 01-JAN-00 0000      0000" 


def test_generate_empty_title():
    assert minimal(generate_title()) == "TITLE" + " " * 5 


def test_generate_non_empty_title():
    assert minimal(generate_title(), lambda x: len(x) > 10) == "TITLE " + " " * 4 + "0"


def test_generate_title_continuation():
    assert minimal(generate_title(continuation_number=5)) == "TITLE  " + " 5 "
