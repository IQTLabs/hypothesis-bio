import pytest
from hypothesis import errors, given

from hypothesis_bio import (
    MAX_ASCII,
    fastq,
    fastq_entry,
    fastq_quality,
    illumina_sequence_identifier,
    nanopore_sequence_identifier,
    protein,
    sequence_identifier,
)

from .minimal import minimal


def test_fastq_quality_smallest_example():
    actual = minimal(fastq_quality())
    expected = ""

    assert actual == expected


def test_fastq_quality_smallest_non_empty_example():
    actual = minimal(fastq_quality(min_size=1))
    expected = "0"

    assert actual == expected


def test_fastq_quality_size_three_with_one_quality_score():
    actual = minimal(fastq_quality(min_size=3, min_score=5, max_score=5))
    expected = "&&&"

    assert actual == expected


def test_fastq_quality_size_three_with_one_quality_score_and_sanger_offset():
    actual = minimal(fastq_quality(min_size=3, min_score=5, max_score=5, offset=64))
    expected = "EEE"

    assert actual == expected


def test_fastq_quality_min_score_larger_than_max_score_raises_error():
    min_score = 10
    max_score = 9
    with pytest.raises(errors.InvalidArgument):
        minimal(fastq_quality(min_score=min_score, max_score=max_score))


def test_fastq_quality_offset_causes_outside_ascii_range_raises_error():
    min_score = 100
    max_score = 101
    with pytest.raises(ValueError):
        minimal(fastq_quality(min_score=min_score, max_score=max_score))


def test_fastq_entry_smallest_example():
    actual = minimal(fastq_entry())
    expected = "@\n\n+\n"

    assert actual == expected


def test_fastq_entry_smallest_non_empty_example():
    actual = minimal(
        fastq_entry(min_size=1, identifier_source=sequence_identifier(min_size=1))
    )
    expected = "@0\nA\n+0\n0"

    assert actual == expected


@given(fastq_entry(min_size=10, max_size=10))
def test_fastq_entry_size_over_one(fastq_string: str):
    fields = fastq_string.split("\n")
    header_begin = fields[0][0]
    assert header_begin == "@"

    seq_id = fields[0][1:]
    seq_id_opt = fields[2][1:]
    if seq_id:
        assert all(33 <= ord(c) <= MAX_ASCII for c in seq_id)
        assert all(33 <= ord(c) <= MAX_ASCII for c in seq_id_opt)

    sequence = fields[1]
    assert len(sequence) == 10

    seq_qual_sep = fields[2][0]
    assert seq_qual_sep == "+"

    quality = fields[-1]
    assert all(33 <= ord(c) <= MAX_ASCII for c in quality)


@given(fastq_entry(min_size=10, max_size=10, additional_description=False))
def test_fastq_entry_size_over_one_with_comment_no_additional_description(
    fastq_string: str
):
    fields = fastq_string.split("\n")
    header_begin = fields[0][0]
    assert header_begin == "@"

    seq_id = fields[0][1:]
    if seq_id:
        assert all(33 <= ord(c) <= MAX_ASCII for c in seq_id)

    sequence = fields[1]
    assert len(sequence) == 10

    seq_qual_sep = fields[2][0]
    assert seq_qual_sep == "+"

    optional_description = fields[2][1:]
    assert not optional_description

    quality = fields[-1]
    assert all(33 <= ord(c) <= MAX_ASCII for c in quality)


@given(
    fastq_entry(
        min_size=10, max_size=10, identifier_source=illumina_sequence_identifier()
    )
)
def test_fastq_entry_size_over_one_with_illumina_id(fastq_string: str):
    fields = fastq_string.split("\n")
    header_begin = fields[0][0]
    assert header_begin == "@"

    seq_id = fields[0][1:]
    assert len(seq_id.split(":")) == 11
    seq_id_opt = fields[2][1:]
    assert len(seq_id_opt.split(":")) == 11

    sequence = fields[1]
    assert len(sequence) == 10

    seq_qual_sep = fields[2][0]
    assert seq_qual_sep == "+"

    quality = fields[-1]
    assert all(33 <= ord(c) <= MAX_ASCII for c in quality)


@given(fastq_entry(min_size=10, max_size=10, wrap_length=3))
def test_fastq_entry_wrapping_less_than_size_wraps_seq_and_quality(fastq_string: str):
    fields = fastq_string.split("\n")

    actual = len(fields)
    expected = 10

    assert actual == expected, fastq_string


@given(fastq_entry(min_size=10, max_size=10, wrap_length=30))
def test_fastq_entry_wrapping_greater_than_size_doesnt_wrap(fastq_string: str):
    fields = fastq_string.split("\n")

    actual = len(fields)
    expected = 4

    assert actual == expected


def test_fastq_entry_minimal_protein_source():
    actual = minimal(fastq_entry(min_size=1, sequence_source=protein(min_size=1)))
    expected = "@\nA\n+\n0"

    assert actual == expected


def test_illumina_seq_id_minimal():
    actual = minimal(illumina_sequence_identifier())
    expected = "0:0:0:0:0:0:0:A+A 1:N:0:A"

    assert actual == expected


@given(illumina_sequence_identifier())
def test_illumina_seq_id_ensure_control_num_is_even_or_zero(seq_id):
    control_num = int(seq_id.split(":")[-2])

    assert control_num % 2 == 0


def test_nanopore_seq_id_minimal():
    actual = minimal(nanopore_sequence_identifier())
    expected = (
        "00000000-0000-0000-0000-000000000000 "
        "runid={} "
        "sampleid=0 "
        "read=0 "
        "ch=0 "
        "start_time=2000-01-01T00:00:00Z"  # Examples from this strategy shrink towards midnight on January 1st 2000.
    ).format("0" * 40)

    assert actual == expected


def test_fastq_minial():
    actual = minimal(fastq())
    expected = "@\n\n+\n"

    assert actual == expected


@given(fastq(entry_source=fastq_entry(wrap_length=0), min_reads=3, max_reads=3))
def test_fastq_min_and_max_reads_the_same_no_wrapping(fastq_file):
    lines = fastq_file.split("\n")

    actual = len(lines)
    expected = 12

    assert actual == expected
