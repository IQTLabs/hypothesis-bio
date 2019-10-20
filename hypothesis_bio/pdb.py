# -*- coding: utf-8 -*-

"""Main module."""

from datetime import date

from hypothesis.strategies import characters, composite, dates, floats, integers, text

ACHAR = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ATOM = "AUCGTNWSMKRYBDHV"
ALPHANUMERIC = ACHAR + "1234567890"


@composite
def generate_date(draw):
    """Generates a value of type Date in PDB format
    """
    sampled_date = draw(dates(min_value=date(1901, 1, 1), max_value=date.today()))
    month = sampled_date.strftime("%b").upper()
    year = sampled_date.strftime("%Y")[2:]
    day = sampled_date.strftime("%d")
    if len(day) == 1:
        day = "0" + day
    return day + "-" + month + "-" + year


@composite
def generate_idcode(draw):
    """Generates a value of type IDCode in PDB format
    """
    first_char = str(draw(integers(min_value=0, max_value=9)))
    last3_char = draw(text(alphabet=ALPHANUMERIC, min_size=3, max_size=3))
    return first_char + last3_char


@composite
def generate_token(draw, min_size=1, max_size=None):
    """Generates a value of type Token in PDB format

    Arguments:
    - `min_size`: Minimum size of the token to be generated
    - `max_size`: Maximum size of the token to be generated
    """
    token = draw(
        text(
            alphabet=characters(min_codepoint=33, max_codepoint=126),
            min_size=min_size,
            max_size=max_size,
        )
    )
    return token + ": "


@composite
def generate_lstring(draw, min_size=1, max_size=None):
    """Generates a value of Type LString in PDB format

    Arguments:
    - `size`: Size of the lstring to be generated.
    """
    return draw(
        text(
            alphabet=characters(min_codepoint=32, max_codepoint=126),
            min_size=min_size,
            max_size=max_size,
        )
    )


@composite
def generate_real(draw, min_value=0.0, max_value=None):
    """Generates a floating point number in Fortran format
    """
    number = draw(floats(min_value=min_value, max_value=max_value))
    return "F" + str(number)


@composite
def generate_specification(
    draw, min_token_size=1, max_token_size=None, min_value_size=1, max_value_size=None
):
    """Generates a specification. Combination of Token and Value
    """
    token = draw(generate_token(min_size=min_token_size, max_size=max_token_size))
    value = draw(generate_lstring(min_size=min_value_size, max_size=max_value_size))
    return token + value


@composite
def generate_header(draw):
    """Generates the Header record in PDB
    """
    classification = draw(generate_lstring(min_size=0, max_size=40))
    depDate = draw(generate_date())
    idCode = draw(generate_idcode())
    return (
        "HEADER" + " " * 3 + classification.ljust(40, " ") + depDate + " " * 3 + idCode
    )


@composite
def generate_obslte(draw, continuation_number=None, min_entries=1, max_entries=9):
    """Generates the Obslte record in PDB

    Arguments:
    - `continuation_number`: The number of obslte record in this PDB entry. Must either be None or >=2
    - `min_entries`: The minimum number of extra obsolete entries to be generated.
    - `max_entries`: The maximum number of extra obsolete entries to be generated.
    """
    generated_record = "OBSLTE "
    if continuation_number is None:
        generated_record += "   "
    else:
        cont_string = str(continuation_number)
        generated_record += cont_string.rjust(2, " ") + " "
    repDate = draw(generate_date())
    generated_record += repDate + " "
    idCode = draw(generate_idcode())
    generated_record += idCode + "      "
    num_entries = draw(integers(min_value=min_entries, max_value=max_entries))
    for i in range(num_entries):
        code = draw(generate_idcode())
        if i < num_entries - 1:
            generated_record += code + " "
        else:
            generated_record += code
    return generated_record


@composite
def generate_title(draw, continuation_number=None):
    """Generates the Title record in PDB

    Arguments:
    - `continuation_number`: The number of Title record in this PDB entry. Must either be None or >=2.
    """
    cont_string = ""
    if continuation_number is None:
        cont_string = "  "
    else:
        cont_string = str(continuation_number).rjust(2, " ") + " "

    title = draw(generate_lstring(min_size=0, max_size=70))
    return "TITLE   " + cont_string + title


@composite
def generate_split(draw, continuation_number=None, min_entries=1, max_entries=14):
    """Generates the Split record in PDB

    Arguments:
    - `continuation_number`: The number of split record in this PDB entry. Must either be None or >=2
    - `min_entries`: The minimum number of entries to be generated.
    - `max_entries`: The maximum number of entries to be generated.
    """
    cont_string = ""
    if continuation_number is None:
        cont_string = "   "
    else:
        cont_string = str(continuation_number).rjust(2, " ") + " "

    num_entries = draw(integers(min_value=min_entries, max_value=max_entries))
    ids_string = ""
    for i in range(num_entries):
        code = draw(generate_idcode())
        if i < num_entries - 1:
            ids_string += code + " "
        else:
            ids_string += code
    return "SPLIT   " + cont_string + ids_string
