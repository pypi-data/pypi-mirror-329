import asyncio
import importlib
import pathlib
import sys
from typing import Protocol, runtime_checkable


@runtime_checkable
class WebsocketServer(Protocol):
    async def run(self): ...


def main():
    args = sys.argv[1]
    split = args.split(".")
    instance = split[-1]
    module = ".".join(split[:-1])

    cur_dir = pathlib.Path().cwd()
    if str(cur_dir) not in sys.path:
        sys.path.insert(0, str(cur_dir))

    module_import = importlib.import_module(module)
    get_instance = getattr(module_import, instance)

    if not isinstance(get_instance, WebsocketServer):
        raise Exception("Not an instance of WebsocketServer")

    asyncio.run(get_instance.run())
