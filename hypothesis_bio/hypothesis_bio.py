# -*- coding: utf-8 -*-

"""Main module."""

from typing import Dict, Optional, Sequence

from hypothesis import assume
from hypothesis.searchstrategy import SearchStrategy
from hypothesis.strategies import characters, composite, integers, sampled_from, text

from .utilities import ambiguous_start_codons, ambiguous_stop_codons, protein_1to3


MAX_ASCII = 126


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
    - `allow_gaps`: Whether a `-` may be in the DNA sequence.
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
def protein(
    draw,
    allow_extended=False,
    allow_ambiguous=True,
    single_letter_protein=True,
    uppercase_only=False,
    min_size=0,
    max_size: Optional[int] = None,
):
    """Generates protein sequences.

    ::: tip Tip
    By default, only canonical amino acids are used.
    :::

    Arguments:
    - `allow_extended`: Whether the extended amino acid alphabet should be used.
    - `allow_ambiguous`: Whether ambiguous amino acids are permitted.
    - `single_letter_protein`: Whether 1-letter or 3-letter abbreviations of proteins should be used.
    - `uppercase_only`: Whether to restrict the protein sequence to uppercase characters.
    - `min_size`: The shortest protein sequence to generate.
    - `max_size`: The longest protein sequence to generate.
    """
    chars = "ACDEFGHIKLMNPQRSTVWY"
    if allow_ambiguous:
        chars += "X"
    if allow_extended:
        chars += "BJOUZ"
    if not uppercase_only:
        chars += chars.lower()
    sequence = draw(text(alphabet=chars, min_size=min_size, max_size=max_size))
    if single_letter_protein:
        return sequence
    else:
        sequence_3 = ""
        for s in sequence:
            sequence_3 += protein_1to3[s]
        return sequence_3


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
    draw, comment_source: SearchStrategy = None, sequence_source: SearchStrategy = None
) -> Dict[str, str]:
    if comment_source is None:
        comment_source = text(alphabet=characters(min_codepoint=32, max_codepoint=126))
    if sequence_source is None:
        sequence_source = dna()

    comment = draw(comment_source)
    sequence = draw(sequence_source)
    return {
        "fasta": ">" + comment + "\n" + sequence,
        "comment": comment,
        "sequence": sequence,
    }


@composite
def kmers(draw, seq: str, k: int) -> str:
    """Generates k-mers (short sliding window substrings) from a given sequence

    Arguments:
    - `seq`: The sequence to be used for generating k-mers
    - `k`: Size of the substrings to be generated
    """
    if len(seq) < k:
        raise ValueError(
            "The value of k: "
            + str(k)
            + " is greater than the length of the sequence: "
            + str(len(seq))
        )

    kmer_index = draw(integers(min_value=0, max_value=len(seq) - k))
    kmer = seq[kmer_index : kmer_index + k]
    return kmer


@composite
def fasta(draw) -> str:
    """Generate strings representing sequences in FASTA format.
    """
    return draw(parsed_fasta())["fasta"]


@composite
def sequence_id(
    draw, blacklist_characters: Sequence[str] = ">@", max_size: int = 100
) -> str:
    """Generates a sequence ID.

    Arguments:
    - `blacklist_character`: Characters to not include in the sequence ID.
    - `max_size`: Maximum length of the sequence ID.
    """
    return draw(
        text(
            alphabet=characters(
                blacklist_characters=blacklist_characters,
                min_codepoint=33,
                max_codepoint=MAX_ASCII,
            ),
            max_size=max_size,
        )
    )


@composite
def fastq_quality(
    draw, size=0, min_score: int = 0, max_score: int = 62, offset: int = 64
) -> str:
    """Generates the quality string for the FASTQ format

    Arguments:
    - `size`: Size of the quality string to be generated
    - `min_score`: Lowest quality (PHRED) score to use.
    - `max_score`: Highest quality (PHRED) score to use.
    - `offset`: ASCII encoding offset.
    for more details.

    Note:
        See https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2847217/ for more details on
        the quality score encoding.
    """
    min_codepoint = min_score + offset
    max_codepoint = max_score + offset

    if max_codepoint > MAX_ASCII:
        raise ValueError(
            "{} is larger than the maximum ASCII value {}".format(
                max_codepoint, MAX_ASCII
            )
        )

    return draw(
        text(
            alphabet=characters(
                min_codepoint=min_codepoint, max_codepoint=max_codepoint
            ),
            min_size=size,
            max_size=size,
        )
    )


@composite
def fastq(
    draw,
    size=0,
    min_score: int = 0,
    max_score: int = 62,
    offset: int = 64,
    add_comment: bool = False,
    additional_description: bool = False,
) -> str:
    """Generate strings representing sequences in FASTQ format.

    Arguments:
    - `size`: Size of the sequence and quality string.
    - `min_score`: Lowest quality (PHRED) score to use.
    - `max_score`: Highest quality (PHRED) score to use.
    - `offset`: ASCII encoding offset for quality string.
    - `add_comment`: Add a comment string after the sequence ID, separated by a space.
    - `additional_description`: Add sequence ID and comment after `+` on thrid line.
    for more details.

    Note:
        See https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2847217/ for more details on
        the FASTQ format (and its quality score encoding).
    """
    seq_id = draw(sequence_id())
    sequence = draw(
        dna(
            allow_ambiguous=False,
            allow_gaps=False,
            uppercase_only=True,
            min_size=size,
            max_size=size,
        )
    )
    comment = " " + draw(sequence_id()) if add_comment else ""
    quality = draw(
        fastq_quality(
            size=size, min_score=min_score, max_score=max_score, offset=offset
        )
    )
    description = seq_id + comment if additional_description else ""

    return "@{seq_id}{comment}\n{sequence}\n+{description}\n{quality}".format(
        seq_id=seq_id,
        sequence=sequence,
        comment=comment,
        quality=quality,
        description=description,
    )
