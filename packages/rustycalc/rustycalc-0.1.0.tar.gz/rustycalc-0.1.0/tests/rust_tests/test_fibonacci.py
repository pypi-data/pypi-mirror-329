import pytest
import rustycalc as rc

@pytest.mark.parametrize(
    "a,b",
    [
        (0,0),
        (1,1),
        (2,1),
        (3,2),
        (4,3),
        (5,5),
        (6,8),
        (7,13),
        (8,21),
        (9,34),
        (10,55)
    ],
)
def test_fib(a,b):
    assert rc.fibonacci(a) == b
