# -*- coding: utf-8 -*-

"""Main module."""

from hypothesis.strategies import composite, text
from hypothesis import assume


@composite
def dna(draw, allow_ambiguous=True, uppercase_only=False, min_size=0, max_size=None):
    """Generates a DNA sequence"""
    chars = "ATGC" if not allow_ambiguous else "ACGTNUKSYMWRBDHV"
    if not uppercase_only:
        chars += chars.lower()
    chars += "-" if allow_ambiguous else ""
    return draw(text(alphabet=chars, min_size=min_size, max_size=max_size))


@composite
def cds(draw, sequence_source=dna(), **kwargs):
    if kwargs:
        sequence_source = dna(**kwargs)
    sequence_source = draw(sequence_source)
    assume(len(sequence_source) % 3 == 0)
    return sequence_source
