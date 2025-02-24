use pyo3::prelude::*;
use pythonize::{depythonize, pythonize};
use serde::{Deserialize, Serialize};

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[derive(Debug, Serialize, Deserialize, PartialEq)]
struct Sample {
    foo: u64,
    bar: Option<usize>,
}

#[pyfunction]
fn rust_sleep<'a>(py: Python<'a>, var: Bound<'a, PyAny>) -> PyResult<Bound<'a, PyAny>> {
    let new_sample: Sample = depythonize(&var).unwrap();
    pyo3_async_runtimes::async_std::future_into_py(py, async move {
        async_std::task::sleep(std::time::Duration::from_secs(new_sample.foo)).await;
        Ok(())
    })
}

/// A Python module implemented in Rust.
#[pymodule]
fn nextgraph(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(rust_sleep, m)?)?;
    Ok(())
}
