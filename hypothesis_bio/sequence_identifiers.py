from typing import Optional, Sequence

from hypothesis import assume
from hypothesis.strategies import (
    characters,
    composite,
    datetimes,
    from_regex,
    integers,
    text,
)

from . import MAX_ASCII


@composite
def sequence_identifier(
    draw,
    blacklist_characters: Sequence[str] = "",
    min_size: int = 0,
    max_size: Optional[int] = None,
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
    No formal specifications could be found, this strategy is based off a header produced from `Guppy` v2.1.3:

        @db127b21-9336-4052-8a8e-5b5d6ac0e3be runid=700c35056d5bf4191f3f9ade0cb342d8406f8ea4 sampleid=madagascar_tb_mdr_3 read=20199 ch=214 start_time=2018-02-26T21:39:56Z

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
