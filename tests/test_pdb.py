from hypothesis_bio.pdb import (
    generate_caveat,
    generate_compnd,
    generate_date,
    generate_header,
    generate_idcode,
    generate_lstring,
    generate_obslte,
    generate_real,
    generate_specification,
    generate_split,
    generate_title,
    generate_token,
)

from .minimal import minimal


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
    assert (
        minimal(generate_obslte(continuation_number=2))
        == "OBSLTE  2 01-JAN-00 0000      0000"
    )


def test_generate_empty_title():
    assert minimal(generate_title()) == "TITLE" + " " * 5


def test_generate_non_empty_title():
    assert minimal(generate_title(), lambda x: len(x) > 10) == "TITLE " + " " * 4 + "0"


def test_generate_title_continuation():
    assert minimal(generate_title(continuation_number=5)) == "TITLE    5 "


def test_generate_non_empty_title_continuation():
    assert (
        minimal(generate_title(continuation_number=5), lambda x: len(x) > 11)
        == "TITLE    5 0"
    )


def test_generate_split():
    assert minimal(generate_split()) == "SPLIT      0000"


def test_generate_split_continuation():
    assert minimal(generate_split(continuation_number=5)) == "SPLIT    5 0000"


def test_generate_caveat():
    assert minimal(generate_caveat()) == "CAVEAT     0000    "


def test_generate_non_empty_caveat():
    assert (
        minimal(generate_caveat(), lambda x: len(x) > 19)
        == "CAVEAT" + " " * 5 + "0000" + "    " + "0"
    )


def test_generate_caveat_continuation():
    assert minimal(generate_caveat(continuation_number=5)) == "CAVEAT   5 0000    "


def test_generate_compnd_molid():
    assert (
        minimal(generate_compnd(), lambda x: "MOL_ID" in x)
    ) == "COMPND     MOL_ID: 0;"
