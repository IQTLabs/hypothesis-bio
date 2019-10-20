from hypothesis_bio.strategy_blast6 import BLAST6_DEFAULT_COL_HEADERS, blast6

from .minimal import minimal


def test_smallest_example():
    args_dict = {}
    for key in BLAST6_DEFAULT_COL_HEADERS.keys():
        args_dict[key] = []
    print(minimal(blast6(args_dict)))
