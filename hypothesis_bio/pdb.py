# -*- coding: utf-8 -*-

"""Main module."""

from datetime import date
from string import ascii_letters, digits

from hypothesis.strategies import (
    booleans,
    characters,
    composite,
    dates,
    floats,
    from_regex,
    integers,
    sampled_from,
    text,
)

ACHAR = ascii_letters
ATOM = "AUCGTNWSMKRYBDHV"
ALPHANUMERIC = ACHAR + digits


@composite
def generate_date(draw):
    """Generates a value of type Date in PDB format
    """
    sampled_date = draw(dates(min_value=date(1901, 1, 1), max_value=date.today()))
    month = sampled_date.strftime("%b").upper()
    year = sampled_date.strftime("%y")
    day = sampled_date.strftime("%d")
    return day + "-" + month + "-" + year


@composite
def generate_idcode(draw):
    """Generates a value of type IDCode in PDB format
    """
    return draw(from_regex(r"[0-9][a-zA-Z0-9]{3}", fullmatch=True))


@composite
def generate_token(draw, min_size=1, max_size=None):
    """Generates a value of type Token in PDB format

    ### Arguments
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

    ### Arguments
    - `min_size`: Minimum Size of the lstring to be generated.
    - `max_size`: Maximum size of the lstring to be generated.
    """
    string = draw(
        text(
            alphabet=characters(min_codepoint=32, max_codepoint=126),
            min_size=min_size,
            max_size=max_size,
        )
    )

    return string.replace(";", "\\;").replace(":", "\\:").replace(",", "\\,")


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

    ### Arguments
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

    ### Arguments
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

    ### Arguments
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


@composite
def generate_caveat(draw, continuation_number=None):
    """Generates the Caveat record in PDB

    ### Arguments
    - `continuation_number`: The number of caveat record in this PDB entry. Must be either None or >=2.
    """
    cont_string = ""
    if continuation_number is None:
        cont_string = "   "
    else:
        cont_string = str(continuation_number).rjust(2, " ") + " "

    code = draw(generate_idcode())
    caveat = draw(generate_lstring(min_size=0, max_size=60))
    return "CAVEAT  " + cont_string + code + "    " + caveat


@composite
def generate_compnd(draw, continuation_number=None):
    """Generates the COMPND record in PDB

    ### Arguments
    - `continuation_number`: The number of caveat record in this PDB entry. Must be either None or >=2.
    """
    record_string = "COMPND "
    cont_string = ""
    if continuation_number is None:
        cont_string = "   "
    else:
        cont_string = str(continuation_number).rjust(2, " ") + " "

    record_string += cont_string + " "

    property_list = [
        "MOL_ID",
        "MOLECULE",
        "CHAIN",
        "FRAGMENT",
        "SYNONYM",
        "EC",
        "ENGINEERED",
        "MUTATION",
        "OTHER_DETAILS",
    ]
    choice = draw(sampled_from(property_list))
    record_string += choice + ": "
    if choice == "MOL_ID":
        val = draw(integers())
        record_string += str(val) + ";"
    elif choice == "MOLECULE":
        char_space_left = 80 - (len(record_string) + 1)
        val = draw(generate_lstring(min_size=1, max_size=char_space_left))
        record_string += val + ";"
    elif choice == "CHAIN":
        char_space_left = 80 - (len(record_string) + 1)
        chain_space_left = int(char_space_left / 3)
        val = draw(integers(min_value=1, max_value=chain_space_left))
        for i in range(val):
            chain = draw(text(alphabet=ACHAR, min_size=1, max_size=1))
            if i == val - 1:
                record_string += chain + ";"
            else:
                record_string += chain + ","
    elif choice == "FRAGMENT":
        # TODO Verify. I have no idea what needs to go here.
        char_space_left = 80 - (len(record_string) + 1)
        val = draw(generate_lstring(min_size=1, max_size=char_space_left))
        record_string += val + ";"
    elif choice == "SYNONYM":
        char_space_left = 80 - (len(record_string) + 1)
        val = draw(generate_lstring(min_size=1, max_size=char_space_left))
        record_string += val + ";"
    elif choice == "ENGINEERED":
        val = draw(booleans())
        if val:
            record_string += "YES;"
        else:
            record_string += "NO;"
    elif choice == "OTHER_DETAILS":
        char_space_left = 80 - (len(record_string) + 1)
        val = draw(generate_lstring(min_size=1, max_size=char_space_left))
        record_string += val + ";"
    elif choice == "MUTATION":
        val = draw(booleans())
        if val:
            record_string += "YES;"
        else:
            record_string += "NO;"
    elif choice == "EC":
        val = draw(booleans())
        if val:
            # TODO: Implement support for multiple ECs
            val1 = draw(integers())
            val2 = draw(integers())
            val3 = draw(integers())
            val4 = draw(integers())
            record_string += (
                str(val1) + "." + str(val2) + "." + str(val3) + "." + str(val4) + ";"
            )
        else:
            record_string += "NUMBER NOT ASSIGNED;"
    return record_string
