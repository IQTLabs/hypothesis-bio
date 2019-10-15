from itertools import product
from typing import List

ambiguous_bases = {
    "A": ["A", "W", "M", "R", "D", "H", "V", "N"],
    "T": ["T", "W", "K", "Y", "B", "D", "H", "N"],
    "G": ["G", "S", "K", "R", "B", "D", "V", "N"],
    "C": ["C", "S", "M", "Y", "B", "H", "V", "N"],
}


def ambiguate_seq(seq: str) -> List[str]:
    return [
        "".join(prod)
        for prod in list(product(*[ambiguous_bases[base] for base in seq]))
    ]


ambiguous_start_codons = ambiguate_seq("ATG")
ambiguous_stop_codons = [
    ambig_stop
    for stop_codon in ["TAA", "TAG", "TGA"]
    for ambig_stop in ambiguate_seq(stop_codon)
]