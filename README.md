# Welcome to Hypothesis-Bio!

Hypothesis extension for computational biology

## Quick Start

### Basic Example

So what exactly does Hypothesis-Bio do?
Let's look at some example code that calculates [GC-content](https://en.wikipedia.org/wiki/GC-content):

```python
def gc_content(seq):
    g_count = seq.count("G") + seq.count("g")
    c_count = seq.count("C") + seq.count("c")
    return (g_count + c_count) / len(seq)
```

(Can you spot the bug in the code?)

Now let's test it out using Hypothesis-Bio.
To do so, we specify a _property_ about our code that we expect to hold true over all examples.
In this case, GC-content is a percentage, so we know it should always be between 0 and 1.
We can encode that requirement into a test:

```python
from hypothesis import given
from hypothesis_bio import dna

@given(dna())
def test_gc_content(seq):
    assert 0 <= gc_content(seq) <= 1
```

When we run the test (by calling `test_gc_content`), we get the following output:

```python
Falsifying example: test_gc_content(seq='')

ZeroDivisionError: division by zero
```

Aha!
When given an empty sequence, our simple `gc_content` calculator raises an error.
This simple example shows the power of property-based testing.
Instead of hard coding inputs and output examples, we can let Hypothesis-Bio do the hard work for us.

### Another Example

We saw that Hypothesis-Bio can catch simple bugs like a division by zero error, but it can do so much more than that.
Let's consider another function that translates from DNA to protein:

```python
genetic_code = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M', 'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K', 'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L', 'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q', 'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V', 'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E', 'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S', 'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*', 'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W'}

def translate(dna):
    protein = ""
    for codon_start_index in range(0, len(dna), 3):
        codon = dna[codon_start_index : codon_start_index + 3]
        protein += genetic_code[codon]
    return protein
```

This looks pretty good, right?
(Hint: nope! Can you find all the bugs?)
For our testing code, we can rely on the property that a DNA sequence's protein is always a third the length of DNA sequence (since three DNA bases are used to code for each amino acid in the protein):

```python
from hypothesis import given
from hypothesis_bio import dna


@given(dna())
def test_translate(seq):
    assert len(translate(seq)) == len(seq) / 3
```

When we run it, we get the following error:

```python
Falsifying example: test_translate(seq='A')

KeyError: 'A'
```

It turns out that our translation function never actually checked to ensure that the DNA sequence was a coding sequence.
If the sequence isn't at least three letters long, there's no way to convert it into a protein.
We should fix our function, but to see just what Hypothesis-Bio can do, we'll tell it the minimum length DNA sequence we want via the `min_size` argument:

```python
@given(dna(min_size=3))
def test_translate(seq):
    assert len(translate(seq)) == len(seq) / 3
```

Now we get this error:

```python
Falsifying example: test_translate(seq='AA-')

KeyError: 'AA-'
```

Whoops, we forgot to take gap characters into account!
Note that Hypothesis didn't just find any example that raised a bug, it found the _smallest_ falsifying example.
Again, while we should fix the `translate` function, let's just ignore the issue to see what else Hypothesis will find:

```python
@given(dna(min_size=3, allow_gaps=False))
def test_translate(seq):
    assert len(translate(seq)) == len(seq) / 3
```

Now we get:

```python
Falsifying example: test_translate(seq='AAB')

KeyError: 'AAB'
```

It turns out we also forgot the ambiguous nucleotides as well.
What else can we find if we ignore ambiguous nucleotides?

```python
@given(dna(min_size=3, allow_gaps=False, allow_ambiguous=False))
def test_translate(seq):
    assert len(translate(seq)) == len(seq) / 3
```

Now we get:

```python
Falsifying example: test_translate(seq='AAa')

KeyError: 'AAa'
```

We also forgot to handle lowercase characters!
By passing the argument `uppercase_only=True` to `dna`, we can tell Hypothesis-Bio to only generate uppercase DNA sequences:

```python
@given(dna(min_size=3, allow_gaps=False, allow_ambiguous=False, uppercase_only=True))
def test_translate(seq):
    assert len(translate(seq)) == len(seq) / 3
```

And now we get:

```python
Falsifying example: test_translate(seq='AAAA')

KeyError: 'A'
```

We now see another bug, in which a sequence whose length isn't divisible by 3 will result in a KeyError since there'll be a partial codon.
Gaps and ambiguous bases and lowercase letters, oh my!
Thankfully, Hypothesis-Bio will generate all of these weird edge cases so you don't manually have to.

## Installation

Hypothesis-Bio will be available from PyPI via

```
pip install hypothesis-bio
```

And Conda using:

```
conda install -c [CHANNEL GOES HERE] hypothesis-bio
```

## Documentation

The documentation for Hypothesis-Bio is available [here](https://lab41.github.io/hypothesis-bio/).

## Citation

If you use Hypothesis-Bio, please cite it as:

```

```

or, for BibTeX:

```bibtex
@misc{hypothesis_bio,
  author    = {Benjamin Lee},
  title     = {{Hypothesis-Bio}},
  publisher = {GitHub},
  url       = {https://github.com/Lab41/hypothesis-bio}
}
```
