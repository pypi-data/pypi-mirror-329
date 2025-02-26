import rustycalc as rc

import pytest


@pytest.mark.parametrize(
    "a,b,c",
    [
        (1,2,3),
        (2,3,5),
        (10,15,25)
    ],
)
def test_sum(a,b,c):
    assert rc.sum(a,b) == c

@pytest.mark.parametrize(
    "a,b,c",
    [
        (1,2,-1),
        (2,1,1),
        (100,15,85)
    ],
)
def test_diff(a,b,c):
    assert rc.diff(a,b) == c
