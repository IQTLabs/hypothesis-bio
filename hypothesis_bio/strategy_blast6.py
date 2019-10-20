# -*- coding: utf-8 -*-

"""Main module."""

from hypothesis.strategies import composite, floats, integers, text

from .utilities import get_characters_source


@composite
def qseqid(draw, min_size=1, max_size=None):
    """Generates the qseqid for Blast+6 file format.

    Arguments:
    - `min_size`: Shortest qseqid to generate.
    - `max_size`: Longest qseqid to generate.
    """
    source = get_characters_source()
    return draw(text(source, min_size=min_size, max_size=max_size))


@composite
def sseqid(draw, min_size=1, max_size=None):
    """Generates the sseqid for Blast+6 file format.

    Arguments:
    - `min_size`: Shortest sseqid to generate.
    - `max_size`: Longest sseqid to generate.
    """
    source = get_characters_source()
    return draw(text(source, min_size=min_size, max_size=max_size))


@composite
def pident(draw, min_value=0.0, max_value=100.0):
    """Generates the pident for Blast+6 file format.

    Arguments:
    - `min_value`: Minimum value of pident to generate.
    - `max_value`: Maximum value of pident to generate.
    """
    return draw(floats(min_value=min_value, max_value=max_value))


@composite
def length(draw, min_value=0, max_value=None):
    """Generates the length for Blast+6 file format.

    Arguments:
    - `min_value`: Minimum value of length to generate.
    - `max_value`: Maximum value of length to generate.
    """
    return draw(integers(min_value=min_value, max_value=max_value))


@composite
def mismatch(draw, min_value=0, max_value=None):
    """Generates the mismatch for Blast+6 file format.

    Arguments:
    - `min_value`: Minimum value of mismatch to generate.
    - `max_value`: Maximum value of mismatch to generate.
    """
    return draw(integers(min_value=min_value, max_value=max_value))


@composite
def gapopen(draw, min_value=0, max_value=None):
    """Generates the gapopen for Blast+6 file format.

    Arguments:
    - `min_value`: Minimum value of gapopen to generate.
    - `max_value`: Maximum value of gapopen to generate.
    """
    return draw(integers(min_value=min_value, max_value=max_value))


@composite
def qstart(draw, min_value=0, max_value=None):
    """Generates the qstart for Blast+6 file format.

    Arguments:
    - `min_value`: Minimum value of qstart to generate.
    - `max_value`: Maximum value of qstart to generate.
    """
    return draw(integers(min_value=min_value, max_value=max_value))


@composite
def qend(draw, min_value=0, max_value=None):
    """Generates the qend for Blast+6 file format.

    Arguments:
    - `min_value`: Minimum value of qend to generate.
    - `max_value`: Maximum value of qend to generate.
    """
    return draw(integers(min_value=min_value, max_value=max_value))


@composite
def sstart(draw, min_value=0, max_value=None):
    """Generates the sstart for Blast+6 file format.

    Arguments:
    - `min_value`: Minimum value of sstart to generate.
    - `max_value`: Maximum value of sstart to generate.
    """
    return draw(integers(min_value=min_value, max_value=max_value))


@composite
def send(draw, min_value=0, max_value=None):
    """Generates the send for Blast+6 file format.

    Arguments:
    - `min_value`: Minimum value of send to generate.
    - `max_value`: Maximum value of send to generate.
    """
    return draw(integers(min_value=min_value, max_value=max_value))


@composite
def evalue(draw, min_value=0.0, max_value=None):
    """Generates the evalue for Blast+6 file format.

    Arguments:
    - `min_value`: Minimum value of evalue to generate.
    - `max_value`: Maximum value of evalue to generate.
    """
    return draw(floats(min_value=min_value, max_value=max_value))


@composite
def bitscore(draw, min_value=0.0, max_value=None):
    """Generates the bitscore for Blast+6 file format.

    Arguments:
    - `min_value`: Minimum value of bitscore to generate.
    - `max_value`: Maximum value of bitscore to generate.
    """
    return draw(floats(min_value=min_value, max_value=max_value))


BLAST6_DEFAULT_COL_HEADERS = {
    "qseqid": qseqid,
    "sseqid": sseqid,
    "pident": pident,
    "length": length,
    "mismatch": mismatch,
    "gapopen": gapopen,
    "qstart": qstart,
    "qend": qend,
    "sstart": sstart,
    "send": send,
    "evalue": evalue,
    "bitscore": bitscore,
}


@composite
def blast6(draw, attribute_args, num_lines=1):
    """Generates the Blast+6 file format.

    Arguments:
    - `attribute_args`: Dictionary mapping attribute names to the list of arguments to be used for generation.
    - `num_lines`: Number of lines to be generated.
    """
    num_attribs = len(attribute_args)
    main_seq = ""
    for i in range(num_lines):
        j = 0
        seq = ""
        for attrib, args in attribute_args.items():
            seq += str(BLAST6_DEFAULT_COL_HEADERS[attrib](*args))
            j += 1
            if j < num_attribs:
                seq += "\t"
        main_seq += seq
        if i < num_lines - 1:
            main_seq += "\n"
    return main_seq
