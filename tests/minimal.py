from __future__ import absolute_import, division, print_function

from hypothesis import HealthCheck, Verbosity, given, settings as Settings
from hypothesis.errors import Unsatisfiable
from hypothesis.internal.reflection import get_pretty_function_description

TIME_INCREMENT = 0.01


class Timeout(BaseException):
    pass


def minimal(definition, condition=lambda x: True, settings=None, timeout_after=10):
    """Generates minimal example of a given strategy.

    This file is directly modified from https://github.com/HypothesisWorks/hypothesis/blob/c3cce7b627f10716b448964fb376fe5626b360c6/hypothesis-python/tests/common/debug.py#L34.
    """

    class Found(Exception):
        """Signal that the example matches condition."""

    def wrapped_condition(x):
        if timeout_after is not None:
            if runtime:
                runtime[0] += TIME_INCREMENT
                if runtime[0] >= timeout_after:
                    raise Timeout()
        result = condition(x)
        if result and not runtime:
            runtime.append(0.0)
        return result

    @given(definition)
    @Settings(
        parent=settings or Settings(max_examples=50000, verbosity=Verbosity.quiet),
        suppress_health_check=HealthCheck.all(),
        report_multiple_bugs=False,
        derandomize=True,
        database=None,
    )
    def inner(x):
        if wrapped_condition(x):
            result[:] = [x]
            raise Found

    definition.validate()
    runtime = []
    result = []
    try:
        inner()
    except Found:
        return result[0]
    raise Unsatisfiable(
        "Could not find any examples from %r that satisfied %s"
        % (definition, get_pretty_function_description(condition))
    )
