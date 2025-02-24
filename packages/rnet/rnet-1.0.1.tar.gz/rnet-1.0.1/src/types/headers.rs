use std::ops::Deref;

use pyo3::{
    prelude::*,
    types::{PyBytes, PyDict},
    IntoPyObjectExt,
};
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};
use rquest::header;

/// A HTTP header map.
///
/// # Examples
///
/// ```python
/// import rnet
/// from rnet import Method
///
/// async def main():
///     resp = await rnet.request(Method.GET, "https://www.google.com/")
///     print("Headers: ", resp.headers.to_dict())
///
/// if __name__ == "__main__":
///     import asyncio
///     asyncio.run(main())
/// ```
#[gen_stub_pyclass]
#[pyclass]
#[derive(Clone)]
pub struct HeaderMap(header::HeaderMap);

#[gen_stub_pymethods]
#[pymethods]
impl HeaderMap {
    /// Converts the header map to a Python dictionary.
    ///
    /// # Returns
    ///
    /// A Python dictionary representing the headers.
    pub fn to_dict<'rt>(&self, py: Python<'rt>) -> PyResult<Bound<'rt, PyDict>> {
        let new_dict = PyDict::new(py);
        for (header, value) in &self.0 {
            new_dict.set_item(header.as_str(), PyBytes::new(py, value.as_ref()))?;
        }
        Ok(new_dict)
    }

    /// Gets the value of the specified header.
    ///
    /// # Arguments
    ///
    /// * `key` - The name of the header.
    ///
    /// # Returns
    ///
    /// An optional byte slice representing the value of the header.
    fn __getitem__(&self, key: &str) -> PyResult<Option<PyObject>> {
        if let Some(value) = self.0.get(key) {
            return Python::with_gil(|py| {
                Ok(value
                    .as_bytes()
                    .into_bound_py_any(py)
                    .map(|b| b.unbind())
                    .ok())
            });
        }

        Ok(None)
    }

    /// Returns a string representation of the header map.
    pub fn __str__(&self) -> String {
        format!("{:?}", self.0)
    }
}

impl From<header::HeaderMap> for HeaderMap {
    fn from(map: header::HeaderMap) -> Self {
        HeaderMap(map)
    }
}

impl Deref for HeaderMap {
    type Target = header::HeaderMap;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}
