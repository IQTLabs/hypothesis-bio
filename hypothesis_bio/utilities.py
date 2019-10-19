from hypothesis.strategies import characters


def get_characters_source():
    return characters(min_codepoint=32, max_code_point=126)


ambiguous_bases = {
    "A": ["A", "W", "M", "R", "D", "H", "V", "N"],
    "T": ["T", "W", "K", "Y", "B", "D", "H", "N"],
    "G": ["G", "S", "K", "R", "B", "D", "V", "N"],
    "C": ["C", "S", "M", "Y", "B", "H", "V", "N"],
}

protein_1to3 = {
    "A": "Ala",
    "C": "Cys",
    "D": "Asp",
    "E": "Glu",
    "F": "Phe",
    "G": "Gly",
    "H": "His",
    "I": "Ile",
    "K": "Lys",
    "L": "Leu",
    "M": "Met",
    "N": "Asn",
    "P": "Pro",
    "Q": "Gln",
    "R": "Arg",
    "S": "Ser",
    "T": "Thr",
    "V": "Val",
    "W": "Trp",
    "Y": "Tyr",
    # Unknown/Unimportant protein
    "X": "Xaa",
    # Extended Proteins
    "B": "Asx",
    "J": "Xle",
    "O": "Pyl",
    "U": "Sec",
    "Z": "Glx",
}

# sorted(list(set([codon for table in [table.start_codons for table in CodonTable.unambiguous_dna_by_id.values()] for codon in table])))
start_codons = ["ATA", "ATC", "ATG", "ATT", "CTG", "GTG", "TTA", "TTG"]
# from Bio.Data import CodonTable
# sorted(list(set([codon for table in [table.start_codons for table in CodonTable.ambiguous_dna_by_id.values()] for codon in table])))
ambiguous_start_codons = [
    "ATA",
    "ATB",
    "ATC",
    "ATD",
    "ATG",
    "ATH",
    "ATK",
    "ATM",
    "ATN",
    "ATR",
    "ATS",
    "ATT",
    "ATV",
    "ATW",
    "ATX",
    "ATY",
    "BTG",
    "CTG",
    "DTG",
    "GTG",
    "HTG",
    "KTG",
    "MTG",
    "NTG",
    "RTG",
    "STG",
    "TTA",
    "TTG",
    "TTR",
    "VTG",
    "WTA",
    "WTG",
    "WTR",
    "XTG",
    "YTG",
]

# sorted(list(set([codon for table in [table.stop_codons for table in CodonTable.unambiguous_dna_by_id.values()] for codon in table])))
stop_codons = ["AGA", "AGG", "TAA", "TAG", "TCA", "TGA", "TTA"]
# sorted(list(set([codon for table in [table.stop_codons for table in CodonTable.ambiguous_dna_by_id.values()] for codon in table])))
ambiguous_stop_codons = [
    "AGA",
    "AGG",
    "AGR",
    "TAA",
    "TAG",
    "TAR",
    "TCA",
    "TDA",
    "TGA",
    "TKA",
    "TMA",
    "TRA",
    "TSA",
    "TTA",
    "TVA",
    "TWA",
]
