import logging.config
import os
import time
from datetime import datetime
from typing import Callable

import yaml
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import FileResponse
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel

DATA_DIR = os.getenv("DATA_DIR", "/Data")

app = FastAPI()

# setup logging
with open("logging.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
logger = logging.getLogger("app")


logger.info(DATA_DIR)


class HealtCheckResponse(BaseModel):
    now: str


@app.on_event("startup")
async def startup():
    """Include metrics exporter on startup of the application."""
    Instrumentator().instrument(app).expose(app)  # include /metrics endpoint


@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable):
    """Add process time to http response header."""
    logger.info(
        f"Received {request.method} request '{request.url}' with "
        f"path_params={request.path_params}; query_params={request.query_params or {} }."
    )

    # process request
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    # include process time
    response.headers["X-Process-Time"] = str(process_time)
    m, s = divmod(int(process_time), 60)
    logger.info(f"Processed a request in {m:02d}:{s:02d} (total seconds = {process_time:.2f}).")

    return response


@app.get("/")
def health_check() -> HealtCheckResponse:
    """Endpoint for checking that the server is running. Returns a response with a current time."""
    return HealtCheckResponse(now=datetime.now().strftime("%d.%m.%Y-%H:%M:%S"))


@app.get("/files/{file_path:path}")
def get_image(file_path: str) -> FileResponse:
    """Endpoint that returns a file in files directory based on the `file_path`."""
    logger.debug(f"{file_path=}")
    if len(file_path) > 0 and file_path[0] == "/":
        file_path = file_path[1:]
    full_file_path = os.path.join(DATA_DIR, file_path)
    logger.debug(f"{full_file_path=}")
    logger.debug(f"isfile={os.path.isfile(full_file_path)}")
    if os.path.isfile(full_file_path):
        out = FileResponse(full_file_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return out
