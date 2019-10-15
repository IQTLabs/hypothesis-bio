# -*- coding: utf-8 -*-

"""Main module."""

from typing import Optional

from hypothesis import assume
from hypothesis.strategies import characters, composite, sampled_from, text

from .utilities import ambiguous_start_codons, ambiguous_stop_codons


@composite
def dna(
    draw,
    allow_ambiguous=True,
    allow_gaps=True,
    uppercase_only=False,
    min_size=0,
    max_size: Optional[int] = None,
):
    """Generates DNA sequences.

    Arguments:
    - `allow_ambiguous`: Whether ambiguous bases are permitted.
    - `allow_gaps`: Whether a `_` may be in the DNA sequence.
    - `uppercase_only`: Whether to use only uppercase characters.
    - `min_size`: The shortest DNA sequence to generate.
    - `max_size`: The longest DNA sequence to generate.
    """

    # decide the character list to use
    chars = "ATGC" if not allow_ambiguous else "ACGTNUKSYMWRBDHV"
    if not uppercase_only:
        chars += chars.lower()
    chars += "-" if allow_gaps else ""

    return draw(text(alphabet=chars, min_size=min_size, max_size=max_size))


@composite
def cds(
    draw,
    allow_ambiguous=True,
    allow_gaps=True,
    uppercase_only=False,
    min_size=0,
    max_size=None,
):
    """Generates [coding DNA sequences](https://en.wikipedia.org/wiki/Coding_region) (CDSs).

    The arguments are the same as for [`dna()`](#dna).
    """
    # we use the same arguments as dna(), since a CDS will be a DNA sequence
    # we don't use kwargs to enable better autocompletion for developer ergonomics
    sequence = draw(
        dna(
            allow_ambiguous=allow_ambiguous,
            allow_gaps=allow_gaps,
            uppercase_only=uppercase_only,
            min_size=min_size,
            max_size=max_size,
        )
    )

    # ensure the sequence is divisible into codons
    assume(len(sequence) % 3 == 0)

    # remove start/stop codons that aren't at the beginning/end
    for codon in range(3, len(sequence) - 3, 3):
        assume(sequence[codon : codon + 3].upper() not in ambiguous_start_codons)
        assume(sequence[codon : codon + 3].upper() not in ambiguous_stop_codons)

    # if we do have a sequence (aka not ''), make sure it has a start and stop codon
    if sequence:
        if allow_ambiguous:
            sequence = (
                draw(sampled_from(ambiguous_start_codons))
                + sequence
                + draw(sampled_from(ambiguous_stop_codons))
            )
        else:
            sequence = "ATG" + sequence + draw(sampled_from(["TAA", "TAG", "TGA"]))

    return sequence


@composite
def parsed_fasta(
    draw,
    comment_source=text(alphabet=characters(min_codepoint=32, max_codepoint=126)),
    sequence_source=dna(),
) -> dict:
    comment = draw(comment_source)
    sequence = draw(sequence_source)
    return {
        "fasta": ">" + comment + "\n" + sequence,
        "comment": comment,
        "sequence": sequence,
    }


@composite
def fasta(draw):
    """Generate strings representing sequences in FASTA format.
    """
    return draw(parsed_fasta())["fasta"]


@composite
def fastq_quality(draw, size=0) -> str:
    """Generates the quality string for the FASTQ format

    Arguments:
    - `size`: Size of the quality string to be generated

    Note:
    According to https://en.wikipedia.org/wiki/FASTQ_format,
    the range of characters for the quality string ranges from
    byte value 0x21 to 0x7E.
    """
    return draw(
        text(
            alphabet=characters(min_codepoint=33, max_codepoint=126),
            min_size=size,
            max_size=size,
        )
    )


@composite
def fastq(draw, fasta_source=parsed_fasta()) -> str:
    """Generate strings representing sequences in FASTQ format.
    """
    fasta_sequence = draw(fasta_source)
    # TODO: randomly wrap the quality string
    quality_string = draw(fastq_quality(size=len(fasta_sequence["sequence"])))
    return (
        "@"
        + fasta_sequence["comment"]
        + "\n"
        + fasta_sequence["sequence"]
        + "\n+"
        # original FASTQ format duplicated the comment (now usually omitted for space)
        + draw(sampled_from(["", fasta_sequence["comment"]]))
        + "\n"
        + quality_string
    )
