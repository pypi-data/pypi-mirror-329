from threading import Timer

from starlette.requests import Request
from fastapi.responses import JSONResponse

from crashless import handler


def handle_exception(request: Request, exc: Exception):
    """Makes sure that messages display in the correct order in the terminal"""
    Timer(interval=0.05, function=handler.threaded_function, args=(exc,)).start()
    return JSONResponse(status_code=500, content=handler.get_content_message(exc))
