# API Reference
Main module.

## `dna()`

```python
@composite
def dna(draw, allow_ambiguous=True, uppercase_only=False, min_size=0, max_size=None)
```

Generates a DNA sequence

## `cds()`

```python
@composite
def cds(draw, sequence_source=dna(), kwargs)
```

Uses dna

__Arguments__

- __`draw`__: hi

