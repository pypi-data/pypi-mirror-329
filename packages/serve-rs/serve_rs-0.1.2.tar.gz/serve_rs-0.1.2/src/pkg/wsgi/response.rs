use pyo3::prelude::*;
use std::sync::Mutex;

// Shared storage for response status and headers
#[pyclass]
pub struct WsgiResponse {
    status: Mutex<Option<String>>,
    headers: Mutex<Vec<(String, String)>>,
}

#[pymethods]
impl WsgiResponse {
    #[new]
    pub fn new() -> Self {
        WsgiResponse {
            status: Mutex::new(None),
            headers: Mutex::new(Vec::new()),
        }
    }

    fn start_response(&self, status: String, headers: Vec<(String, String)>) {
        let mut status_lock = self.status.lock().unwrap();
        let mut headers_lock = self.headers.lock().unwrap();
        *status_lock = Some(status);
        *headers_lock = headers;
    }
}
