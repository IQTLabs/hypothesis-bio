from hypothesis import given

from hypothesis_bio.hypothesis_bio import fasta
from hypothesis_bio.to_filehandler import test_biopython, test_scikit


@given(fasta())
def test_scikit_file(seq):
    assert test_scikit(seq, "fasta") == True


def test_scikit_file_false():
    assert test_scikit(">\n", "fasta") == False


@given(fasta())
def test_biopython_file(seq):
    assert test_biopython(seq, "fasta") == True


def test_biopython_file_false():
    assert test_biopython("xsa\nKEOW", "fasta") == False
