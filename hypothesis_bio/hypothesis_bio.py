# -*- coding: utf-8 -*-

"""Main module."""

from hypothesis.strategies import composite, text, characters
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


@composite
def fasta(
    draw,
    comment_source=text(alphabet=characters(min_codepoint=32, max_codepoint=126)),
    sequence_source=dna(),
    **kwargs
):
    """Generate strings representing sequences in FASTA format.
    """
    if kwargs:
        sequence_source = dna(**kwargs)
    comment = draw(comment_source)
    assume("\\n" not in comment)
    return ">" + comment + "\n" + draw(sequence_source)
