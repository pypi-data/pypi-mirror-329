use hyper::{
    service::{make_service_fn, service_fn}, Server
};
use pyo3::{exceptions::PyValueError, prelude::*};
use tokio::signal;
use std::{convert::Infallible, net::SocketAddr, sync::Arc};

use crate::pkg::wsgi::WSGIApp;

pub async fn serve(path: &str) -> PyResult<()>{
    let (wsgi_module, wsgi_app) = if let Some((module, app)) = path.split_once(':') {
        (module, app)    
    } else {
        return Err(PyValueError::new_err("Invalid path format"));
    };
    
    let app = Arc::new(Python::with_gil(|py|{
        WSGIApp::new(py, wsgi_module, wsgi_app)
    })?);
    
    let addr = SocketAddr::from(([127, 0, 0, 1], 8000));
    let make_svc = make_service_fn(move |_| {
        let app = app.clone();
        async { 
            Ok::<_, Infallible>(service_fn(move |req| {
                let app = app.clone();
                async move {
                    app.handle_request(req).await 
                }
            }))
        }
    });

    println!("WSGI Server running at http://{}", addr);
    let server = Server::bind(&addr).serve(make_svc);
    tokio::select! {
        _ = server => {},
        _ = signal::ctrl_c() => {}
    }
    Ok(())
}
