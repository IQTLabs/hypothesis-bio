from hypothesis_bio import dna 
from hypothesis import given
from hypothesis import assume
from hypothesis.strategies import SearchStrategy, characters, composite, integers, sampled_from, text, floats, just, booleans
from hypothesis_bio import fasta_entry
from hypothesis_bio import fasta
import pydna
import pyviko

from tests.minimal import minimal


valid_types = [
    "SO:0000000",
    "Sequence Ontology",
    "SO:0000001",
    "region",
    "SO:0000004",
    "interior coding exon",
    "SO:0000005",
    "satellite DNA",
    "SO:0000006",
    "PCR product",
    "SO:0000007",
    "read pair",
    "SO:0000013",
    "scRNA",
    "SO:0000038",
    "match set",
    "SO:0000039",
    "match part",
    "SO:0000050",
    "gene part",
    "SO:0000057",
    "operator",
    "SO:0000059",
    "nuclease binding site",
    "SO:0000101",
    "transposable element",
    "SO:0000102",
    "expressed sequence match",
    "SO:0000103",
    "clone insert end",
    "SO:0000104",
    "polypeptide",
    "SO:0000109",
    "sequence variant obs",
    "SO:0000110",
    "sequence feature",
    "SO:0000112",
    "primer",
    "SO:0000113",
    "proviral region",
    "SO:0000114",
    "methylated C",
    "SO:0000120",
    "protein coding primary transcript",
    "SO:0000139",
    "ribosome entry site",
    "SO:0000140",
    "attenuator",
    "SO:0000141",
    "terminator",
    "SO:0000143",
    "assembly component",
    "SO:0000147",
    "exon",
    "SO:0000148",
    "supercontig",
    "SO:0000149",
    "contig",
    "SO:0000150",
    "read",
    "SO:0000151",
    "clone",
    "SO:0000159",
    "deletion",
    "SO:0000161",
    "methylated A",
    "SO:0000162",
    "splice site",
    "SO:0000163",
    "five prime cis splice site",
    "SO:0000163",
    "five prime splice site",
    "SO:0000164",
    "three prime cis splice site",
    "SO:0000164",
    "three prime splice site",
    "SO:0000165",
    "enhancer",
    "SO:0000167",
    "promoter",
    "SO:0000177",
    "cross genome match",
    "SO:0000178",
    "operon",
    "SO:0000179",
    "clone insert start",
    "SO:0000181",
    "translated nucleotide match",
    "SO:0000183",
    "non transcribed region",
    "SO:0000185",
    "primary transcript",
    "SO:0000187",
    "repeat family",
    "SO:0000188",
    "intron",
    "SO:0000193",
    "RFLP fragment",
    "SO:0000195",
    "coding exon",
    "SO:0000196",
    "five prime coding exon coding region",
    "SO:0000196",
    "five prime exon coding region",
    "SO:0000197",
    "three prime coding exon coding region",
    "SO:0000197",
    "three prime exon coding region",
    "SO:0000198",
    "noncoding exon",
    "SO:0000200",
    "five prime coding exon",
    "SO:0000203",
    "UTR",
    "SO:0000204",
    "five prime UTR",
    "SO:0000205",
    "three prime UTR",
    "SO:0000209",
    "rRNA primary transcript",
    "SO:0000233",
    "mature transcript",
    "SO:0000234",
    "mRNA",
    "SO:0000235",
    "TF binding site",
    "SO:0000236",
    "ORF",
    "SO:0000239",
    "flanking region",
    "SO:0000252",
    "rRNA",
    "SO:0000253",
    "tRNA",
    "SO:0000274",
    "snRNA",
    "SO:0000275",
    "snoRNA",
    "SO:0000276",
    "miRNA",
    "SO:0000289",
    "microsatellite",
    "SO:0000294",
    "inverted repeat",
    "SO:0000296",
    "origin of replication",
    "SO:0000303",
    "clip",
    "SO:0000305",
    "modified base",
    "SO:0000305",
    "modified base site",
    "SO:0000306",
    "methylated base feature",
    "SO:0000307",
    "CpG island",
    "SO:0000314",
    "direct repeat",
    "SO:0000315",
    "TSS",
    "SO:0000316",
    "CDS",
    "SO:0000318",
    "start codon",
    "SO:0000319",
    "stop codon",
    "SO:0000324",
    "tag",
    "SO:0000325",
    "rRNA large subunit primary transcript",
    "SO:0000326",
    "SAGE tag",
    "SO:0000330",
    "conserved region",
    "SO:0000331",
    "STS",
    "SO:0000332",
    "coding conserved region",
    "SO:0000333",
    "exon junction",
    "SO:0000334",
    "nc conserved region",
    "SO:0000336",
    "pseudogene",
    "SO:0000337",
    "RNAi reagent",
    "SO:0000340",
    "chromosome",
    "SO:0000341",
    "chromosome band",
    "SO:0000343",
    "match",
    "SO:0000344",
    "splice enhancer",
    "SO:0000345",
    "EST",
    "SO:0000347",
    "nucleotide match",
    "SO:0000349",
    "protein match",
    "SO:0000353",
    "sequence assembly",
    "SO:0000360",
    "codon",
    "SO:0000366",
    "insertion site",
    "SO:0000368",
    "transposable element insertion site",
    "SO:0000370",
    "small regulatory ncRNA",
    "SO:0000372",
    "enzymatic RNA",
    "SO:0000374",
    "ribozyme",
    "SO:0000375",
    "rRNA 5 8S",
    "SO:0000375",
    "rRNA 5.8S",
    "SO:0000380",
    "hammerhead ribozyme",
    "SO:0000385",
    "RNase MRP RNA",
    "SO:0000386",
    "RNase P RNA",
    "SO:0000390",
    "telomerase RNA",
    "SO:0000391",
    "U1 snRNA",
    "SO:0000392",
    "U2 snRNA",
    "SO:0000393",
    "U4 snRNA",
    "SO:0000394",
    "U4atac snRNA",
    "SO:0000395",
    "U5 snRNA",
    "SO:0000396",
    "U6 snRNA",
    "SO:0000397",
    "U6atac snRNA",
    "SO:0000398",
    "U11 snRNA",
    "SO:0000399",
    "U12 snRNA",
    "SO:0000403",
    "U14 snoRNA",
    "SO:0000404",
    "vault RNA",
    "SO:0000405",
    "Y RNA",
    "SO:0000407",
    "rRNA 18S",
    "SO:0000409",
    "binding site",
    "SO:0000410",
    "protein binding site",
    "SO:0000412",
    "restriction fragment",
    "SO:0000413",
    "sequence difference",
    "SO:0000418",
    "signal peptide",
    "SO:0000419",
    "mature protein region",
    "SO:0000436",
    "ARS",
    "SO:0000441",
    "ss oligo",
    "SO:0000442",
    "ds oligo",
    "SO:0000454",
    "rasiRNA",
    "SO:0000462",
    "pseudogenic region",
    "SO:0000464",
    "decayed exon",
    "SO:0000468",
    "golden path fragment",
    "SO:0000472",
    "tiling path",
    "SO:0000474",
    "tiling path fragment",
    "SO:0000483",
    "nc primary transcript",
    "SO:0000484",
    "three prime coding exon noncoding region",
    "SO:0000486",
    "five prime coding exon noncoding region",
    "SO:0000499",
    "virtual sequence",
    "SO:0000502",
    "transcribed region",
    "SO:0000551",
    "polyA signal sequence",
    "SO:0000553",
    "polyA site",
    "SO:0000577",
    "centromere",
    "SO:0000581",
    "cap",
    "SO:0000587",
    "group I intron",
    "SO:0000588",
    "autocatalytically spliced intron",
    "SO:0000590",
    "SRP RNA",
    "SO:0000593",
    "C D box snoRNA",
    "SO:0000602",
    "guide RNA",
    "SO:0000603",
    "group II intron",
    "SO:0000605",
    "intergenic region",
    "SO:0000610",
    "polyA sequence",
    "SO:0000611",
    "branch site",
    "SO:0000612",
    "polypyrimidine tract",
    "SO:0000616",
    "transcription end site",
    "SO:0000624",
    "telomere",
    "SO:0000625",
    "silencer",
    "SO:0000627",
    "insulator",
    "SO:0000628",
    "chromosomal structural element",
    "SO:0000643",
    "minisatellite",
    "SO:0000644",
    "antisense RNA",
    "SO:0000645",
    "antisense primary transcript",
    "SO:0000646",
    "siRNA",
    "SO:0000649",
    "stRNA",
    "SO:0000650",
    "small subunit rRNA",
    "SO:0000651",
    "large subunit rRNA",
    "SO:0000652",
    "rRNA 5S",
    "SO:0000653",
    "rRNA 28S",
    "SO:0000655",
    "ncRNA",
    "SO:0000657",
    "repeat region",
    "SO:0000658",
    "dispersed repeat",
    "SO:0000662",
    "spliceosomal intron",
    "SO:0000667",
    "insertion",
    "SO:0000668",
    "EST match",
    "SO:0000673",
    "transcript",
    "SO:0000684",
    "nuclease sensitive site",
    "SO:0000687",
    "deletion junction",
    "SO:0000688",
    "golden path",
    "SO:0000689",
    "cDNA match",
    "SO:0000694",
    "SNP",
    "SO:0000695",
    "reagent",
    "SO:0000696",
    "oligo",
    "SO:0000699",
    "junction",
    "SO:0000700",
    "remark",
    "SO:0000701",
    "possible base call error",
    "SO:0000702",
    "possible assembly error",
    "SO:0000703",
    "experimental result region",
    "SO:0000704",
    "gene",
    "SO:0000705",
    "tandem repeat",
    "SO:0000706",
    "trans splice acceptor site",
    "SO:0000714",
    "nucleotide motif",
    "SO:0000715",
    "RNA motif",
    "SO:0000717",
    "reading frame",
    "SO:0000719",
    "ultracontig",
    "SO:0000724",
    "oriT" "SO:0000725",
    "transit peptide",
    "SO:0000727",
    "CRM",
    "SO:0000730",
    "gap",
    "SO:0000752",
    "gene group regulatory region",
    "SO:0000753",
    "clone insert",
    "SO:0000777",
    "pseudogenic rRNA",
    "SO:0000778",
    "pseudogenic tRNA",
    "SO:0000830",
    "chromosome part",
    "SO:0000831",
    "gene member region",
    "SO:0000833",
    "transcript region",
    "SO:0000834",
    "mature transcript region",
    "SO:0000835",
    "primary transcript region",
    "SO:0000836",
    "mRNA region",
    "SO:0000837",
    "UTR region",
    "SO:0000839",
    "polypeptide region",
    "SO:0000841",
    "spliceosomal intron region",
    "SO:0000842",
    "gene component region",
    "SO:0000851",
    "CDS region",
    "SO:0000852",
    "exon region",
    "SO:0001000",
    "rRNA 16S",
    "SO:0001001",
    "rRNA 23S",
    "SO:0001002",
    "rRNA 25S",
    "SO:0001019",
    "copy number variation",
    "SO:0001037",
    "mobile genetic element",
    "SO:0001039",
    "integrated mobile genetic element",
    "SO:0001055",
    "transcriptional cis regulatory region",
    "SO:0001056",
    "splicing regulatory region",
    "SO:0001059",
    "sequence alteration",
    "SO:0001063",
    "immature peptide region",
    "SO:0001214",
    "noncoding region of exon",
    "SO:0001215",
    "coding region of exon",
    "SO:0001235",
    "replicon",
    "SO:0001236",
    "base",
    "SO:0001248",
    "assembly",
    "SO:0001409",
    "biomaterial region",
    "SO:0001410",
    "experimental feature",
    "SO:0001411",
    "biological region",
    "SO:0001412",
    "topologically defined region",
    "SO:0001419",
    "cis splice site",
    "SO:0001420",
    "trans splice site",
    "SO:0001483",
    "SNV",
    "SO:0001527",
    "peptide localization signal",
    "SO:0001647",
    "kozak sequence",
    "SO:0001654",
    "nucleotide to protein binding site",
    "SO:0001679",
    "transcription regulatory region",
    "SO:0001683",
    "sequence motif",
    "SO:0001720",
    "epigenetically modified region",
    "SO:0001790",
    "paired end fragment",
    "SO:0005836",
    "regulatory region",
    "SO:0005855",
    "gene group",
    "SO:0100011",
    "cleaved peptide region",
    "SO:1000002",
    "substitution",
    "SO:1000005",
    "complex substitution",
    "SO:1000008",
    "point mutation",
    "SO:1000036",
    "inversion",
    "SO:1001284",
    "regulon",
    "SO:2000061",
    "databank entry",
]

@composite
def gff_attributes(draw):
    results = []
    num_tags = draw(integers(min_value = 0))
    if not num_tags:
        return "."
    for i in range(num_tags):
        results.append(draw(text(alphabet=characters(min_codepoint=32, max_codepoint=126), min_size = 1)) + '=' + draw(text(alphabet=characters(min_codepoint=32, max_codepoint=126), min_size = 1)))

    return ';'.join(results)

@composite
def gff_entry(
    draw,
    seqid = None,
    source = None,
    the_type = None,
    start = None,
    end = None,
    score = None,
    strand = None,
    phase = None,
    attributes = None
) -> str:
    gff = []
    if seqid is None:
        gff.append(draw(text(alphabet=characters(min_codepoint=32, max_codepoint=126), min_size = 1)))
    else:
        gff.append(seqid)

    if source is None:
        gff.append(draw(text(alphabet=characters(min_codepoint=32, max_codepoint=126), min_size = 1)))
    else:
        gff.append(source)
        
    if the_type is None:
        gff.append(draw(text(alphabet=characters(min_codepoint=32, max_codepoint=126), min_size = 1)))
        #hardcode the various SOFA catergories into a list
    else:
        gff.append(the_type)

    if start is None:
        gff.append(str(draw(integers(min_value = 1))))
    else:
        gff.append(start)
   
    if end is None:
        gff.append(str(draw(integers(min_value = int(gff[-1])))))
    else:
        gff.append(end)
    
    if score is None:
        gff.append(str(draw(floats())))
        #could be a period
    else:
        gff.append(score)

    if strand is None:
        gff.append((draw(sampled_from(['+', '-']))))
    else:
        gff.append(strand)

    if phase is None:
        gff.append((draw(sampled_from(['0', '1', '2', '.']))))
    else:
        gff.append(phase)

    if attributes is None:
        gff.append(draw(gff_attributes()))
        #find a way to generate attributes (found in GFF documentation)
    else:
        gff.append(attributes)
    
    return '\t'.join(gff)

@composite
def multiple_gff_entries(draw, fasta = True):
    commentline = "##gff-version 3 \n"
    entries = []
    for i in range(draw(integers(min_value = 3))):
        entries.append(draw(gff_entry()))
    gff = commentline + '\n'.join(entries)
    #if (fasta is None and draw(booleans())) or (fasta):
    #    gff += draw(add_fasta_to_gff(gff))
    return gff

    #return commentline + '\n'.join(entries)

@composite
def add_fasta_to_gff(draw, gff_file):
    seqids = []
    fasta_list = []
    # for line in gff_file.split('\n'):
    #     if line.startswith('#'):
    #         continue
    #     seqids.append(line.split('\t')[0])
    # print(seqids)
    # for seqid in set(seqids):
    #    #fasta = draw(fasta_entry(comment_source = just(seqid)))
    #    fasta = ""
    #    fasta_list.append(fasta)
    return '##FASTA' + '\n'.join(fasta_list)

@given(multiple_gff_entries())
def test_multiple_gff_entries(gff_file):
    #print(gff_file)
    #assert gff_file.count('>') < 5
    assert len(gff_file) < 50

#@given(gff_entry())
#def test_gff(gff_entry):
#   print(gff_entry)
#   assert gff_entry.count('=') < 3
   

#given seqid, find the largest sequence end (minimum should be defaulted to this largest feature stop coordinate of this largest sequence)





    












