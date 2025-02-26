from rustycalc._core import hello_from_bin, fibonacci, factorial
from rustycalc.addition.sum import sum
from rustycalc.subtraction.diff import diff

def hello() -> str:
    return hello_from_bin()

__all__ = [
    'hello_from_bin',
    'factorial',
    'fibonacci',
    'sum',
    'diff',
]

def goal():
    print("work hard, party harder, fuck much harder.")