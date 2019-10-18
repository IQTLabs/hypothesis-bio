from .minimal import minimal
import hypothesis
import pytest
from hypothesis_bio.hypothesis_bio import fastq, fastq_quality


def test_fastq_quality_smallest_example():
    actual = minimal(fastq_quality())
    expected = ""

    assert actual == expected


def test_fastq_quality_smallest_non_empty_with_default_ascii():
    actual = minimal(fastq_quality(size=1))
    expected = "@"

    assert actual == expected


def test_fastq_quality_size_three_with_one_quality_score():
    actual = minimal(fastq_quality(size=3, min_score=5, max_score=5))
    expected = "EEE"

    assert actual == expected


def test_fastq_quality_size_three_with_one_quality_score_and_sanger_offset():
    actual = minimal(fastq_quality(size=3, min_score=5, max_score=5, offset=33))
    expected = "&&&"

    assert actual == expected


def test_fastq_quality_min_score_larger_than_max_score_raises_error():
    min_score = 10
    max_score = 9
    with pytest.raises(hypothesis.errors.InvalidArgument):
        minimal(fastq_quality(min_score=min_score, max_score=max_score))


def test_fastq_quality_offset_causes_outside_ascii_range_raises_error():
    min_score = 100
    max_score = 101
    offset = 200
    with pytest.raises(ValueError):
        minimal(fastq_quality(min_score=min_score, max_score=max_score))


def test_fastq_smallest_example():
    actual = minimal(fastq())
    expected = "@\n\n+\n"

    assert actual == expected
