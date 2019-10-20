from hypothesis import given

from hypothesis_bio import dna, fasta, fasta_entry

from .minimal import minimal


@given(fasta_entry())
def test_return_type(seq):
    assert type(seq) == str


@given(fasta_entry(wrap_length=5))
def test_wrap_length(seq):
    assert all(
        [len(x.rstrip()) == 5 for x in seq.split("\n")[:-1] if not x.startswith(">")]
    )


@given(fasta_entry(allow_windows_line_endings=False))
def test_no_windows_line_endings(seq):
    assert "\r" not in seq


@given(
    fasta_entry(
        comment_source=dna(
            uppercase_only=True, allow_ambiguous=False, allow_gaps=False
        ),
        sequence_source=dna(
            uppercase_only=True, allow_ambiguous=False, allow_gaps=False
        ),
    )
)
def test_sources(seq):
    assert set(seq).issubset({"\r", "\n", "A", "T", "G", "C", ">"})


def test_fasta_minimal():
    actual = minimal(fasta())
    expected = ">\n"

    assert actual == expected


@given(fasta(entry_source=fasta_entry(wrap_length=5), min_reads=3, max_reads=3))
def test_fasta_min_and_max_reads_the_same_no_wrapping(fasta_file):
    lines = fasta_file.split("\n")

    actual = len(lines)
    expected = 6

    assert actual == expected
