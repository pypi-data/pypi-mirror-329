mod cmd;
mod pkg;

use pkg::server::serve;
use pyo3::prelude::*;
use tokio::runtime::Runtime;

#[pyfunction]
fn start(py: Python, path: &str, port: u16) -> PyResult<()> {
    py.allow_threads(||{
        tokio::task::block_in_place(move || {
            let rt = Runtime::new().expect("failed");
            rt.block_on(async {
                serve(&path, port).await.unwrap();     
            });
        });
        Ok(())
    })
}

#[pymodule]
fn servers(m: &Bound<'_, PyModule>) -> PyResult<()> {
    tracing_subscriber::fmt::init();
    m.add_function(wrap_pyfunction!(start, m)?)?;
    Ok(())
}
