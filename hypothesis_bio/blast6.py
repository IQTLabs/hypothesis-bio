# -*- coding: utf-8 -*-

"""Constants for generating BLAST+6 files."""

from hypothesis.strategies import characters, floats, from_type

BLAST6_HEADERS = {
    "qseqid": characters(min_codepoint=32, max_codepoint=126),
    "qgi": from_type(int),
    "qacc": characters(min_codepoint=32, max_codepoint=126),
    "qaccver": characters(min_codepoint=32, max_codepoint=126),
    "qlen": from_type(int),
    "sseqid": characters(min_codepoint=32, max_codepoint=126),
    "sallseqid": characters(min_codepoint=32, max_codepoint=126),
    "sgi": from_type(int),
    "sallgi": from_type(int),
    "sacc": characters(min_codepoint=32, max_codepoint=126),
    "saccver": characters(min_codepoint=32, max_codepoint=126),
    "sallacc": characters(min_codepoint=32, max_codepoint=126),
    "slen": from_type(int),
    "qstart": from_type(int),
    "qend": from_type(int),
    "sstart": from_type(int),
    "send": from_type(int),
    "qseq": characters(min_codepoint=32, max_codepoint=126),
    "sseq": characters(min_codepoint=32, max_codepoint=126),
    "evalue": floats(allow_infinity=False),
    "bitscore": floats(allow_infinity=False),
    "score": from_type(int),
    "length": from_type(int),
    "pident": floats(allow_infinity=False),
    "nident": from_type(int),
    "mismatch": from_type(int),
    "positive": from_type(int),
    "gapopen": from_type(int),
    "gaps": from_type(int),
    "ppos": floats(allow_infinity=False),
    "frames": characters(min_codepoint=32, max_codepoint=126),
    "qframe": from_type(int),
    "sframe": from_type(int),
    "btop": from_type(int),
    "staxids": characters(min_codepoint=32, max_codepoint=126),
    "sscinames": characters(min_codepoint=32, max_codepoint=126),
    "scomnames": characters(min_codepoint=32, max_codepoint=126),
    "sblastnames": characters(min_codepoint=32, max_codepoint=126),
    "sskingdoms": characters(min_codepoint=32, max_codepoint=126),
    "stitle": characters(min_codepoint=32, max_codepoint=126),
    "scharacters(min_codepoint=32, max_codepoint=126)and": str,
    "salltitles": characters(min_codepoint=32, max_codepoint=126),
    "qcovs": from_type(int),
    "qcovhsp": from_type(int),
}
"""Dictionary mapping BLAST+6 column names to strategies for generating them.

Modified from the spec provided by [scikit-bio](http://scikit-bio.org/docs/0.5.4/generated/skbio.io.format.blast6.html).
To use with [hypothesis-CSV](https://github.com/chobeat/hypothesis-csv), try:

```python
from hypothesis_csv.strategies import csv

@given(csv(columns=[BLAST6_HEADERS["btop"], BLAST6_HEADERS["stitle"]], dialect="excel-tab")
def test_blast6(blast6):
    ...
```
"""

BLAST6_DEFAULT_HEADERS = [
    BLAST6_HEADERS["qseqid"],
    BLAST6_HEADERS["sseqid"],
    BLAST6_HEADERS["pident"],
    BLAST6_HEADERS["length"],
    BLAST6_HEADERS["mismatch"],
    BLAST6_HEADERS["gapopen"],
    BLAST6_HEADERS["qstart"],
    BLAST6_HEADERS["qend"],
    BLAST6_HEADERS["sstart"],
    BLAST6_HEADERS["send"],
    BLAST6_HEADERS["evalue"],
    BLAST6_HEADERS["bitscore"],
]
"""List of strategies to generate the default BLAST+6 headers.
Useful to use as input to the `columns` keyword argument to `hypothesis-csv`'s `csv` function.
"""
