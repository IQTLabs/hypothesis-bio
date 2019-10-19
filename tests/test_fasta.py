from hypothesis import given

from hypothesis_bio import dna, fasta


@given(fasta())
def test_return_type(seq):
    assert type(seq) == str


@given(fasta(wrap_length=5))
def test_wrap_length(seq):
    assert max([len(x.rstrip()) for x in seq.split("\n") if not x.startswith(">")]) <= 5


@given(fasta(allow_windows_line_endings=False))
def test_no_windows_line_endings(seq):
    assert "\r" not in seq


@given(
    fasta(
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
