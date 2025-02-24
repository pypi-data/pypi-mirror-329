
## Running Your WSGI App (Without the Hassle)  

So you have a WSGI web app, say `django` or `flask` 
Navigate to your project directory and check for a WSGI entry point.  

```bash  
(base) ashutoshpednekar@192 svc % ls | grep mana  
manage.py  
(base) ashutoshpednekar@192 svc % ls main/ | grep wsg  
wsgi.py  
```  

Now, unlike Gunicorn, where you have to decide between **sync, async, gevent, eventlet, tornado, uvicorn workers**  
(seriously, why are there so many worker models?), **serve-rs** just *works*:  

```bash  
(base) ashutoshpednekar@192 svc % serve-rs main.wsgi:application  
[2025-02-22T06:16:50Z INFO  pubsub::common::nats::conn] stream updated successfully  
WSGI Server running at http://127.0.0.1:8000  
```  

No `--workers`, no `--preload`, no `"which worker model should I use?"`—just **run your server(s)**.  
(Yes, that pun was intentional.)  

## cURL away 

```bash  
ashu@ashu:~ $ curl http://localhost:8000/screenmgmt/screen/  
{"errors":[{"code":"ER-0014","detail":"Project is not selected. Please select the project to continue.","attr":null}]}  
```  

