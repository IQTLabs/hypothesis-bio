from textwrap import fill
from typing import Optional

from hypothesis import assume
from hypothesis.searchstrategy import SearchStrategy
from hypothesis.strategies import (
    characters,
    composite,
    datetimes,
    from_regex,
    integers,
    text,
)

from . import MAX_ASCII
from .fasta import sequence_identifier
from .sequences import dna


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
