use pyo3::prelude::*;

#[pyfunction]
pub fn fibonacci(n: u32) -> u32 {
    if n < 2 {
        return n;
    }
    return fibonacci(n-1) + fibonacci(n-2); // not using dynamic programming for now (tabulation)
}

