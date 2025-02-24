# Websocket Consumer

Run an embedded websocket server from the root of your project folder.

```bash
pip install websocket-consumer
```
```bash
uv add websocket-consumer
```

```bash
websocket-consumer app.websockets.server
```

`app = Main package`
`websockets = Sub package`
`server = Instance that passes the WebsocketServer(Protocol)`

## Info

Say you have the following project structure below and are running your wsgi 
and websocket server side by side.

```
app/
├── wsgi/...
└── websockets/
    ├── __init__.py
    ├── __main__.py
    └── server.py
```

In the `__main__.py` file you have the code needed to start the websockets 
server.

If you try and import anything above the websockets package an exception 
will be raised. This is because when you run `python3 app/websockets` the 
project root folder is not included in `sys.path`. 

This project fixes that by allowing you to define an instance of a 
WebSocket class.

## How it works

Create your websocket server as class:

```python
import typing as t

from websockets.asyncio.server import serve


class WebsocketServer:
    host: str = "120.0.0.1"
    port: int = 5003
    connections: t.Set = set()

    def __init__(self, host: str = "120.0.0.1", port: int = 5003):
        self.host = host
        self.port = port

    async def handler(self, websocket):
        ...

    async def run(self):
        async with serve(self.handler, self.host, self.port) as server:
            await server.serve_forever()
```

You must have an async `run()` method on the class as this is what will be 
called at run.

Now create an instance of your websocket server, here's an example:

`app/websockets/__init__.py`
```python
from app.websockets.server import WebsocketServer

server = WebsocketServer(
    host='127.0.0.1',
    port=5003
)
```

Now call the consumer:

```bash
websocket_consumer app.websocket.server
```
