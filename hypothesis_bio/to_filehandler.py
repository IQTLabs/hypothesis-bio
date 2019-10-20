from io import StringIO

from skbio import read
from Bio import SeqIO


def test_scikit(seq="", type="fasta"):
    # type in ['fasta', 'fastq','blast6']
    fh = StringIO(seq)
    try:
        skbio.io.read(fh, format=type)
    except (skbio.io._exception.FASTAFormatError, skbio.io._exception.FASTQFormatError):
        return False
    return True


def test_biopython(seq="", type="fasta"):
    fh = StringIO(seq)
    try:
        x = SeqIO.parse(fh, type)
    except SeqIO.FASTAFormatError:
        return False
    return not len(list(x)) == 0


"""

https://stackoverflow.com/questions/8577137/how-can-i-create-a-tmp-file-in-python
list(skbio.io.read([">a\nAAA"], format="fasta"))[0]

"""
