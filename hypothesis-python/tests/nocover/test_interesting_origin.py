# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Most of this work is copyright (C) 2013-2021 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
#
# END HEADER

import pytest

from hypothesis import given, strategies as st
from hypothesis.errors import MultipleFailures


def go_wrong_naive(a, b):
    try:
        assert a + b < 100
        a / b
    except Exception:
        # Hiding the actual problem is terrible, but this pattern can make sense
        # if you're raising a library-specific or semantically meaningful error.
        raise ValueError("Something went wrong")


def go_wrong_with_cause(a, b):
    try:
        assert a + b < 100
        a / b
    except Exception as err:
        # Explicit chaining is the *right way* to change exception type.
        raise ValueError("Something went wrong") from err


def go_wrong_coverup(a, b):
    try:
        assert a + b < 100
        a / b
    except Exception:
        # This pattern SHOULD be local enough that it never distinguishes
        # errors in practice... but if it does, we're ready.
        raise ValueError("Something went wrong") from None


@pytest.mark.parametrize(
    "function",
    [go_wrong_naive, go_wrong_with_cause, go_wrong_coverup],
    ids=lambda f: f.__name__,
)
def test_can_generate_specified_version(function):
    try:
        given(st.integers(), st.integers())(function)()
    except MultipleFailures:
        pass
    else:
        raise AssertionError("Expected MultipleFailures")
