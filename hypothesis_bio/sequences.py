from typing import Optional

from hypothesis import assume
from hypothesis.strategies import composite, integers, sampled_from, text

from .utilities import (
    ambiguous_start_codons,
    ambiguous_stop_codons,
    protein_1to3,
    start_codons,
    stop_codons,
)


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
    allow_ambiguous=True,
    allow_gaps=True,
    allow_lowercase=True,
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
            sequence_3 += protein_1to3[s.upper()]
        return sequence_3.upper() if uppercase_only else sequence_3


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
        for codon in range(
            3 if include_start_codon else 0,
            len(sequence) - (3 if include_stop_codon else 0),
            3,
        ):
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
