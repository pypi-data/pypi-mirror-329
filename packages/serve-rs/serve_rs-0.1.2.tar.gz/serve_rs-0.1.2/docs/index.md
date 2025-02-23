# serve-rs: A Gunicorn Replacement That won't make you cry  

## What is serve-rs?  

Gunicorn served us well—until it didn’t. Between its *million* worker models, process juggling, and config gymnastics,  
deploying a WSGI app often felt like a side quest. **serve-rs** changes that.  

Built on **Tokio** and **Hyper**, serve-rs is a modern, Rust-powered WSGI server that’s:  

✅ **Simple** – No more tweaking worker models for the nth time  
✅ **Effortless** – Works out of the box with Django, Flask, and friends  

And yes, **ASGI support is on the roadmap**—because it’s 2025, and WSGI alone isn’t cutting it anymore.  

## How It Works  

- **Rust-powered core** – serve-rs uses **Hyper** for high-performance HTTP handling and **Tokio** for async scheduling.  
- **WSGI-compatible** – Hooks into WSGI entry points, so existing apps work with zero changes.  
- **Planned ASGI support** – Future versions will support ASGI frameworks like FastAPI and Starlette.  

### Want to know more?  

Check out [the blog](https://example.com/serve-rs-blog) for deep dives, benchmarks, and future plans. (coming soon) 

## Why You’ll Never Look at Gunicorn Again  

- **No more endless worker models** – You don’t have to Google *"Gunicorn workers explained like I'm five"*.  
- **Processes? In 2025?** – In the age of **containers and serverless**, why are you still micromanaging worker PIDs?  
- **Rust-powered speed** – Because Python’s GIL has slowed you down enough already.  
- **Dead simple deployment** – You don’t need an entire config file just to start your server.  
- **Works with Django** – Because you already have enough problems dealing with it.  

### TL;DR: Run `serve-rs` and get back to building your app.  
