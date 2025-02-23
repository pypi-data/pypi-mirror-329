use std::collections::HashMap;
use hyper::{
   Body, Request, Response 
};
use pyo3::{prelude::*, types::{PyBytes, PyDict}};

use crate::pkg::wsgi::response::WsgiResponse;

use super::WSGIApp;


impl WSGIApp{

    pub async fn handle_request(&self, req: Request<Body>) -> PyResult<Response<Body>> {
        tracing::info!("req: {:?}", &req);

        let path = req.uri().to_string();
        let method = req.method().to_string().to_uppercase();
        let headers: HashMap<String, String> = req.headers()
            .iter()
            .map(|(k, v)| {
                let key = format!("HTTP_{}", k.as_str().replace("-", "_").to_uppercase());
                let value = v.to_str().unwrap_or("").to_string();
                (key, value)
            })
            .collect();
        let body_bytes = hyper::body::to_bytes(req.into_body())
            .await
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{}", e)))?
            .to_vec();


        let app = self.app.clone();
        let port = self.port.clone();

        let (status, response_headers, body) = tokio::task::spawn_blocking(move || {
            Python::with_gil(|py| -> PyResult<(u16, Vec<(String, String)>, Vec<u8>)> {
                let environ = PyDict::new(py);
                for (k, v) in headers.into_iter(){
                    environ.set_item(k.as_str().replace("-", "_").to_uppercase(), v.to_string())?;
                }
                environ.set_item("SERVER_NAME", "")?;
                environ.set_item("SERVER_PORT", port)?;
                environ.set_item("HTTP_HOST", "localhost")?;
                environ.set_item("PATH_INFO", path)?;
                environ.set_item("REQUEST_METHOD", method)?;

                let py_body = PyBytes::new(py, &body_bytes);

                let io = py.import("io")?;
                let wsgi_input = io.getattr("BytesIO")?.call1((py_body,))?;
                environ.set_item("wsgi.input", wsgi_input)?;

                environ.set_item("wsgi.version", (1, 0))?;
                environ.set_item("wsgi.errors", py.None())?;

                tracing::debug!("prepared environ: {:?}", environ);

                let wsgi_response = Py::new(py, WsgiResponse::new())?;
                let start_response = wsgi_response.getattr(py, "start_response")?;
                let res = app.call1(py, (environ, start_response, ))?;
                tracing::info!("called Python WSGI function");

                let status_code = wsgi_response
                    .getattr(py, "get_status")?
                    .call0(py)?
                    .extract::<String>(py)?
                    .split_whitespace()
                    .next()
                    .and_then(|s| s.parse::<u16>().ok())
                    .unwrap_or_default();
                tracing::info!("status code: {}", &status_code);

                tracing::info!("res: {:?}", &res);
                let response_bytes: Vec<u8> = res
                    .getattr(py, "content")?
                    .extract::<Vec<u8>>(py)?;
                Ok((status_code, vec![], response_bytes))   
            })
        }).await.map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))??;

        tracing::info!("{:?}| {:?} | {:?}", status, response_headers, body);
        
        let mut builder = Response::builder().status(status);
        for (key, value) in response_headers {
            //builder = builder.header(&key, &value);
        }
        
        Ok(builder.body(Body::from(body)).unwrap())
    }
}

