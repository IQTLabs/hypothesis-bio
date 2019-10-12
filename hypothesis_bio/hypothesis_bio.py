# -*- coding: utf-8 -*-

"""Main module."""

import hypothesis.strategies as st


@st.composite
def dna(draw, allow_ambiguous=True, uppercase_only=False, min_size=0, max_size=None):
    """Generates a DNA sequence"""
    chars = "ATGC" if not allow_ambiguous else "ACGTNUKSYMWRBDHV"
    if not uppercase_only:
        chars += chars.lower()
    chars += "-" if allow_ambiguous else ""
    return draw(st.text(alphabet=chars, min_size=min_size, max_size=max_size))
