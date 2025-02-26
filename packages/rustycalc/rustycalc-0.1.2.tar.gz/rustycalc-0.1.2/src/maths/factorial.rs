use pyo3::prelude::*;

#[pyfunction]
/// Computes the factorial of a given integer `n`.
pub fn factorial(n: u32) -> u32 {
    if n == 0 {
        return 1;
    }
    return n * factorial(n - 1);
}
