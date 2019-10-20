from textwrap import fill
from typing import Optional, Sequence

from hypothesis import assume
from hypothesis.searchstrategy import SearchStrategy
from hypothesis.strategies import characters, composite, integers, sampled_from, text

from . import MAX_ASCII
from .sequences import dna


@composite
def fasta(
    draw,
    comment_source: SearchStrategy = None,
    sequence_source: SearchStrategy = None,
    wrap_length: Optional[int] = None,
    allow_windows_line_endings=True,
) -> str:
    """Generates FASTA sequences.

    Arguments:
    - `comment_source`: The source of the comments. Defaults to `text(alphabet=characters(min_codepoint=32, max_codepoint=126))`)
    - `sequence_source`: The source of the sequence. Defaults to [`dna`](#dna).
    - `wrap_length`: The width to wrap the sequence on. If `None`, mixed sizes are used.
    - `allow_windows_line_endings`: Whether to allow `\\r\\n` in the linebreaks.
    """
    if comment_source is None:
        comment_source = text(alphabet=characters(min_codepoint=32, max_codepoint=126))
    if sequence_source is None:
        sequence_source = dna()

    comment = draw(comment_source)
    sequence = draw(sequence_source)

    # the nice case where the user gave the wrap size
    if wrap_length is not None:
        sequence = fill(sequence, wrap_length, break_on_hyphens=False)

    # the pathological case
    elif wrap_length is None:

        # choose where to wrap
        indices = [
            draw(integers(min_value=0, max_value=len(sequence)))
            for i in range(draw(integers(min_value=0, max_value=len(sequence))))
        ]
        indices = list(set(indices))

        # randomly put in the line endings
        for index in indices:
            line_ending = (
                draw(sampled_from(["\r\n", "\n"]))
                if allow_windows_line_endings
                else "\n"
            )
            sequence = sequence[:index] + line_ending + sequence[index:]

    # sanity checks
    assume("\n\r" not in sequence and "\n\n" not in sequence and "\r\r" not in sequence)
    assume(not sequence.startswith("\r") and not sequence.startswith("\n"))

    return ">" + comment + "\n" + sequence


@composite
def sequence_identifier(
    draw,
    blacklist_characters: Sequence[str] = "",
    min_size: int = 1,
    max_size: int = 100,
) -> str:
    """Generates a sequence identifier.

    Arguments:
    - `blacklist_characters`: Characters to not include in the sequence ID.
    - `min_size`: Minimum length of the sequence ID.
    - `max_size`: Maximum length of the sequence ID.
    """
    return draw(
        text(
            alphabet=characters(
                blacklist_characters=blacklist_characters,
                min_codepoint=33,
                max_codepoint=MAX_ASCII,
            ),
            min_size=min_size,
            max_size=max_size,
        )
    )
