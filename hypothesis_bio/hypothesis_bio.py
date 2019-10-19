# -*- coding: utf-8 -*-

"""Main module."""

from textwrap import wrap
from typing import Optional, Sequence

from hypothesis import assume
from hypothesis.searchstrategy import SearchStrategy
from hypothesis.strategies import characters, composite, integers, sampled_from, text

from .utilities import (
    ambiguous_start_codons,
    ambiguous_stop_codons,
    protein_1to3,
    start_codons,
    stop_codons,
)

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
def rna(
    draw,
    allow_ambiguous=False,
    allow_gaps=False,
    allow_lowercase=False,
    min_size=0,
    max_size: Optional[int] = None,
):
    """Generates RNA sequences.

    Arguments:
    - `allow_ambiguous`: Whether ambiguous bases are permitted.
    - `allow_gaps`: Whether a `-` may be in the RNA sequence.
    - `allow_lowercase`: Whether lowercase characters should be used.
    - `min_size`: The shortest RNA sequence to generate
    - `max_size`: The longest RNA sequence to generate
    """

    chars = "AUCG" if not allow_ambiguous else "AUCGNTWSMKRYBDHV"
    if allow_lowercase:
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
def start_codon(draw, allow_ambiguous=True) -> str:
    """Strategy to generate [start codons](https://en.wikipedia.org/wiki/Start_codon).

    Arguments:
    - `allow_ambiguous`: Whether ambiguous bases are permitted.
    """
    return draw(
        sampled_from(ambiguous_start_codons if allow_ambiguous else start_codons)
    )


@composite
def stop_codon(draw, allow_ambiguous=True) -> str:
    """Strategy to generate [stop codons](https://en.wikipedia.org/wiki/Stop_codon).

    Arguments:
    - `allow_ambiguous`: Whether ambiguous bases are permitted.
    """
    return draw(sampled_from(ambiguous_stop_codons if allow_ambiguous else stop_codons))


@composite
def cds(
    draw,
    include_start_codon=True,
    include_stop_codon=True,
    allow_internal_stop_codons=True,
    allow_ambiguous=True,
    uppercase_only=False,
    min_size=0,
    max_size=None,
) -> str:
    """Generates [coding DNA sequences](https://en.wikipedia.org/wiki/Coding_region) (CDSs).

    Arguments:
    - `include_start_codon`: Whether to include a [start codon](#start_codon) at the beginning.
    - `include_stop_codon`: Whether to include a [stop codon](#stop_codon) at the end.
    - `allow_internal_stop_codons`: Whether stop codons may occur at any place other than the end.
    - `allow_ambiguous`: Whether ambiguous bases are permitted.
    - `uppercase_only`: Whether to use only uppercase characters.
    - `min_size`: The shortest CDS to generate in base pairs.
    - `max_size`: The longest CDS to generate in base pairs.
    """

    # ensure that what we're trying to do is even possible
    min_possible_size = 0
    if include_start_codon:
        min_possible_size += 3
    if include_stop_codon:
        min_possible_size += 3
    if max_size is not None and max_size < min_possible_size:
        raise ValueError("Sequence is to short to include start/stop codons.")

    # first, create the main DNA sequence
    if include_start_codon:
        min_size -= 3
        if max_size is not None:
            max_size -= 3
    if include_stop_codon:
        min_size -= 3
        if max_size is not None:
            max_size -= 3

    # make sure that the sizes are not negative
    min_size = max(0, min_size)
    if max_size is not None:
        max_size = max(0, max_size)

    sequence = draw(
        dna(
            allow_ambiguous=allow_ambiguous,
            allow_gaps=False,
            uppercase_only=uppercase_only,
            min_size=min_size,
            max_size=max_size,
        )
    )
    assume(len(sequence) % 3 == 0)

    # remove stop codons that aren't at the end if requested
    if not allow_internal_stop_codons:
        for codon in range(3, len(sequence) - 3, 3):
            assume(sequence[codon : codon + 3].upper() not in ambiguous_start_codons)

    # now determine start/stop codons
    if include_start_codon:
        _start_codon = draw(start_codon(allow_ambiguous=allow_ambiguous))
    else:
        _start_codon = ""
    if include_stop_codon:
        _stop_codon = draw(stop_codon(allow_ambiguous=allow_ambiguous))
    else:
        _stop_codon = ""

    return _start_codon + sequence + _stop_codon


@composite
def fasta(
    draw,
    comment_source: SearchStrategy = None,
    sequence_source: SearchStrategy = None,
    wrap_length: Optional[int] = None,
    allow_windows_line_endings=True,
) -> str:

    if comment_source is None:
        comment_source = text(alphabet=characters(min_codepoint=32, max_codepoint=126))
    if sequence_source is None:
        sequence_source = dna()

    comment = draw(comment_source)
    sequence = draw(sequence_source)

    # the nice case where the user gave the wrap size
    if wrap_length is not None:
        sequence = wrap(sequence, width=wrap_length)
        sequence = "\n".join(sequence)

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
def sequence_id(
    draw, blacklist_characters: Sequence[str] = ">@", max_size: int = 100
) -> str:
    """Generates a sequence ID.

    Arguments:
    - `blacklist_characters`: Characters to not include in the sequence ID.
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

    Note:
        See <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2847217/> for more details on
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
    add_comment: bool = True,
    additional_description: bool = True,
) -> str:
    """Generate strings representing sequences in FASTQ format.

    Arguments:
    - `size`: Size of the sequence and quality string.
    - `min_score`: Lowest quality (PHRED) score to use.
    - `max_score`: Highest quality (PHRED) score to use.
    - `offset`: ASCII encoding offset for quality string.
    - `add_comment`: Add a comment string after the sequence ID, separated by a space.
    - `additional_description`: Add sequence ID and comment after `+` on third line.

    Note:
        See <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2847217/> for more details on
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
