# -*- coding: utf-8 -*

"""Strategies for generating [FASTA](https://en.wikipedia.org/wiki/FASTA_format) formatted sequences."""

from textwrap import fill
from typing import Optional

from hypothesis import assume
from hypothesis.searchstrategy import SearchStrategy
from hypothesis.strategies import characters, composite, integers, sampled_from, text

from .sequences import dna


@composite
def fasta_entry(
    draw,
    comment_source: SearchStrategy = None,
    sequence_source: SearchStrategy = None,
    wrap_length: Optional[int] = None,
    allow_windows_line_endings=True,
) -> str:
    """Generates individual FASTA entries.

    ::: warning Warning
    Unless you specifically want to generate single FASTA-formatted entries, use [`fasta`](#fasta) instead when testing code that expects FASTA strings.
    :::

    ### Arguments

    - `comment_source`: The source of the comments. Defaults to `text(alphabet=characters(min_codepoint=32, max_codepoint=126))`)
    - `sequence_source`: The source of the sequence. Defaults to [`dna`](#dna).
    - `wrap_length`: The width to wrap the sequence on. If `None`, mixed sizes are used.
    - `allow_windows_line_endings`: Whether to allow `\\r\\n` in the linebreaks.
    """
    if comment_source is None:
        comment_source = text(alphabet=characters(min_codepoint=32, max_codepoint=126))
    if sequence_source is None:
        sequence_source = dna()

    comment = draw(comment_source)
    sequence = draw(sequence_source)

    # the nice case where the user gave the wrap size
    if wrap_length is not None:
        # default to 80 if wrap length is set as 0
        if wrap_length <= 0:
            wrap_length = 80
        sequence = fill(sequence, wrap_length, break_on_hyphens=False)

    # the pathological case
    elif wrap_length is None:

        # choose where to wrap
        indices = [
            draw(integers(min_value=0, max_value=len(sequence)))
            for i in range(draw(integers(min_value=0, max_value=len(sequence))))
        ]
        indices = list(set(indices))

        # randomly put in the line endings
        for index in indices:
            line_ending = (
                draw(sampled_from(["\r\n", "\n"]))
                if allow_windows_line_endings
                else "\n"
            )
            sequence = sequence[:index] + line_ending + sequence[index:]

    # sanity checks
    assume("\n\r" not in sequence and "\n\n" not in sequence and "\r\r" not in sequence)
    assume(not sequence.startswith("\r") and not sequence.startswith("\n"))

    return ">" + comment + "\n" + sequence


@composite
def fasta(
    draw,
    entry_source: Optional[SearchStrategy] = None,
    min_reads: int = 1,
    max_reads: int = 100,
) -> str:
    """Generates string representations of FASTA files.

    ### Arguments
    - `entry_source`: The search strategy to use for generating FASTA entries. The default (`None`) will use [`fasta_entry`](#fasta_entry) with default settings.
    - `min_reads`: Minimum number of FASTA entries to generate.
    - `max_reads`: Maximum number of FASTA entries to generate.
    """
    if entry_source is None:
        entry_source = fasta_entry()

    num_reads = draw(integers(min_value=min_reads, max_value=max_reads))

    return "\n".join([draw(entry_source) for i in range(num_reads)])
