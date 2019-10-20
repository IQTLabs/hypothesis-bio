# User Guide

::: warning TODO

Finish this section

:::

## Working with other Hypothesis extensions

A lot of biological data formats are tab or comma delimited.
For example, consider default BLAST+6 formatted outputs which are just tab-delimited files like this:

```
moaC	gi|15800534|ref|NP_286546.1|	100.00	161	0	0	1	161	1	161	3e-114330
moaC	gi|170768970|ref|ZP_02903423.1|	99.38	161	1	0	1	161	1	161	9e-114329
```

The [`hypothesis-csv`](https://github.com/chobeat/hypothesis-csv) package is capable of generating tab-delimited files if given a list of the type of each column.
Hypothesis-Bio provides just such a list.
Going back to the BLAST+6 example, you can use the `BLAST6_DEFAULT_HEADERS` list to generate BLAST+6 files:

```python
from hypothesis_bio import BLAST6_DEFAULT_HEADERS
from hypothesis_csv.strategies import csv


@given(csv(columns=BLAST6_DEFAULT_HEADERS, dialect="excel-tab"))
def test_blast6(blast6):
    ...
```
