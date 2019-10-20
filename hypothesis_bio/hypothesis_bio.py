# -*- coding: utf-8 -*-

"""Main module."""

from textwrap import fill
from typing import Optional, Sequence

from hypothesis import assume
from hypothesis.searchstrategy import SearchStrategy
from hypothesis.strategies import (
    characters,
    composite,
    datetimes,
    from_regex,
    integers,
    sampled_from,
    text,
)

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
def fasta_entry(
    draw,
    comment_source: SearchStrategy = None,
    sequence_source: SearchStrategy = None,
    wrap_length: Optional[int] = None,
    allow_windows_line_endings=True,
) -> str:
    """Generates FASTA sequences.

    Arguments:
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
        if wrap_length > 0:
            pass
        else:
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
    """Generates a string representation of a fasta file.

    Arguments:
    - `entry_source`: The search strategy to use for generating fasta entries. The
    default (`None`) will use [`fasta_entry`](#fasta_entry) with default settings.
    - `min_reads`: Minimum number of fasta entries to generate.
    - `max_reads`: Maximum number of fasta entries to generate.
    """
    if entry_source is None:
        entry_source = fasta_entry()

    num_reads = draw(integers(min_value=min_reads, max_value=max_reads))

    return "\n".join([draw(entry_source) for i in range(num_reads)])


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
def sequence_identifier(
    draw,
    blacklist_characters: Sequence[str] = "",
    min_size: int = 1,
    max_size: int = 100,
) -> str:
    """Generates a sequence identifier.

    Arguments:
    - `blacklist_characters`: Characters to not include in the sequence ID.
    - `min_size`: Minimum length of the sequence ID.
    - `max_size`: Maximum length of the sequence ID.
    """
    return draw(
        text(
            alphabet=characters(
                blacklist_characters=blacklist_characters,
                min_codepoint=33,
                max_codepoint=MAX_ASCII,
            ),
            min_size=min_size,
            max_size=max_size,
        )
    )


@composite
def illumina_sequence_identifier(draw) -> str:
    """Generate an Illumina-style sequence identifier.

    ::: tip Note
    Specifications taken from Specifications taken from [here](https://support.illumina.com/help/BaseSpace_Sequence_Hub/Source/Informatics/BS/FileFormat_FASTQ-files_swBS.htm)
    :::
    """
    delim = ":"
    instrument = draw(from_regex(r"[a-zA-Z0-9_]+", fullmatch=True))
    run_number = draw(integers(min_value=0))
    flowcell_id = draw(from_regex(r"[a-zA-Z0-9]+", fullmatch=True))
    lane = draw(integers(min_value=0))
    tile = draw(integers(min_value=0))
    x_pos = draw(integers(min_value=0))
    y_pos = draw(integers(min_value=0))
    umi = draw(from_regex(r"[ACGTN]+\+[ACGTN]+", fullmatch=True))
    read_num = draw(from_regex(r"[12]", fullmatch=True))
    is_filtered = draw(from_regex(r"[YN]", fullmatch=True))
    control_num = draw(integers(min_value=0))
    assume(control_num % 2 == 0)  # control_num must be 0 or even
    index = draw(from_regex(r"[ACGTN]+", fullmatch=True))

    return (
        "{instrument}{delim}{run_number}{delim}{flowcell_id}{delim}{lane}{delim}"
        "{tile}{delim}{x_pos}{delim}{y_pos}{delim}{umi} {read_num}{delim}"
        "{is_filtered}{delim}{control_num}{delim}{index}"
    ).format(
        instrument=instrument,
        delim=delim,
        run_number=run_number,
        flowcell_id=flowcell_id,
        lane=lane,
        tile=tile,
        x_pos=x_pos,
        y_pos=y_pos,
        umi=umi,
        read_num=read_num,
        is_filtered=is_filtered,
        control_num=control_num,
        index=index,
    )


@composite
def nanopore_sequence_identifier(draw) -> str:
    """Generate a Nanopore-style sequence identifier.

    ::: tip Note
        No formal specifications could be found, so am going off a header produced from
        `Guppy` v2.1.3: @db127b21-9336-4052-8a8e-5b5d6ac0e3be runid=700c35056d5bf4191f3f9ade0cb342d8406f8ea4 sampleid=madagascar_tb_mdr_3 read=20199 ch=214 start_time=2018-02-26T21:39:56Z
    :::
    """
    read_id = draw(
        from_regex(
            r"[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}",
            fullmatch=True,
        )
    )
    run_id = draw(from_regex(r"[a-zA-Z0-9]{40}", fullmatch=True))
    sample_id = draw(from_regex(r"[!-~]+", fullmatch=True))
    read_num = draw(integers(min_value=0))
    channel = draw(integers(min_value=0))
    date_time = draw(datetimes())
    start_time = date_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    return (
        "{read_id} runid={run_id} sampleid={sample_id} read={read_num} "
        "ch={channel} start_time={start_time}"
    ).format(
        read_id=read_id,
        run_id=run_id,
        sample_id=sample_id,
        read_num=read_num,
        channel=channel,
        start_time=start_time,
    )


@composite
def fastq_quality(
    draw,
    min_size: int = 1,
    max_size: Optional[int] = None,
    min_score: int = 0,
    max_score: int = 93,
    offset: int = 33,
) -> str:
    """Generates the quality string for the FASTQ format

    Arguments:
    - `min_size`: Minimum length of the quality string.
    - `max_size`: Maximum length of the quality string.
    - `min_score`: Lowest quality (PHRED) score to use.
    - `max_score`: Highest quality (PHRED) score to use.
    - `offset`: ASCII encoding offset.

    ::: tip Note
        The default quality string is 'fastq-sanger' format. If you would like 'fastq-illumina'
        then set `offset` to 64 and `max_score` to 62. If you would like `fastq-solexa`
        then set `offset` to 64, `min_score` to -5 and `max_score` to 62.
        See <https://academic.oup.com/nar/article/38/6/1767/3112533> for more details on
        the FASTQ format (and its quality score encoding).
    :::
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
            min_size=min_size,
            max_size=max_size,
        )
    )


@composite
def fastq_entry(
    draw,
    min_size: int = 1,
    max_size: Optional[int] = None,
    min_score: int = 0,
    max_score: int = 93,
    offset: int = 33,
    sequence_source: Optional[SearchStrategy] = None,
    identifier_source: Optional[SearchStrategy] = None,
    additional_description: bool = True,
    wrap_length: int = 80,
) -> str:
    """Generate an entry in FASTQ format.

    Arguments:
    - `min_size`: Minimum length of the sequence and quality string.
    - `max_size`: Maximum length of the sequence and quality string.
    - `min_score`: Lowest quality (PHRED) score to use.
    - `max_score`: Highest quality (PHRED) score to use.
    - `offset`: ASCII encoding offset for quality string.
    - `sequence_source`: Search strategy to generate the sequence from. By default
    [`dna()`](#dna) will be used.
    - `identifier_source`: Search strategy to generate the sequence identifier from. If
    `None` then random text will be generated.
    - `additional_description`: Add sequence ID and comment after `+` on third line.
    - `wrap_length`: Number of characters to wrap the sequence and quality strings on. Set
    to 0 to disable wrapping.

    ::: tip Note
        The default quality string is 'fastq-sanger' format. If you would like 'fastq-illumina'
        then set `offset` to 64 and `max_score` to 62. If you would like `fastq-solexa`
        then set `offset` to 64, `min_score` to -5 and `max_score` to 62.
        See <https://academic.oup.com/nar/article/38/6/1767/3112533> for more details on
        the FASTQ format (and its quality score encoding).
    :::
    """
    if identifier_source is None:
        identifier_source = sequence_identifier()
    if sequence_source is None:
        sequence_source = dna(min_size=min_size, max_size=max_size)

    seq_id = draw(identifier_source)
    sequence = draw(sequence_source)

    quality = draw(
        fastq_quality(
            min_size=len(sequence),
            max_size=len(sequence),
            min_score=min_score,
            max_score=max_score,
            offset=offset,
        )
    )
    assume(len(quality) == len(sequence))

    description = seq_id if additional_description else ""

    if wrap_length > 0:
        sequence = fill(sequence, wrap_length, break_on_hyphens=False)
        quality = fill(quality, wrap_length, break_on_hyphens=False)

    return "@{seq_id}\n{sequence}\n+{description}\n{quality}".format(
        seq_id=seq_id, sequence=sequence, quality=quality, description=description
    )


@composite
def fastq(
    draw,
    entry_source: Optional[SearchStrategy] = None,
    min_reads: int = 1,
    max_reads: int = 100,
) -> str:
    """Generates a string representation of a fastq file.

    Arguments:
    - `entry_source`: The search strategy to use for generating fastq entries. The
    default (`None`) will use [`fastq_entry`](#fastq_entry) with default settings.
    - `min_reads`: Minimum number of fastq entries to generate.
    - `max_reads`: Maximum number of fastq entries to generate.
    """
    if entry_source is None:
        entry_source = fastq_entry()

    num_reads = draw(integers(min_value=min_reads, max_value=max_reads))

    return "\n".join([draw(entry_source) for i in range(num_reads)])
