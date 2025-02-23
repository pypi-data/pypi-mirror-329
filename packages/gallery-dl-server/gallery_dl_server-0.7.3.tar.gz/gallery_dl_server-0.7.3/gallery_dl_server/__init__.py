# -*- coding: utf-8 -*-

import os
import multiprocessing
import queue
import asyncio
import signal
import shutil
import time

from contextlib import asynccontextmanager
from types import FrameType

from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.datastructures import UploadFile
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response, RedirectResponse, JSONResponse, StreamingResponse
from starlette.requests import Request
from starlette.routing import Route, WebSocketRoute, Mount
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_303_SEE_OTHER
from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState

import aiofiles
import watchfiles
import gallery_dl.version
import yt_dlp.version

from . import download, output, utils, version


log_file = output.LOG_FILE

log = output.initialise_logging(__name__)
blank = output.get_blank_logger()

blank_sent = False


async def redirect(request: Request):
    return RedirectResponse(url="/gallery-dl")


async def homepage(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_version": version.__version__,
            "gallery_dl_version": gallery_dl.version.__version__,
            "yt_dlp_version": yt_dlp.version.__version__,
        },
    )


async def submit_form(request: Request):
    global blank_sent

    if not blank_sent:
        blank.info("")
        blank_sent = True

    form_data = await request.form()

    url = form_data.get("url")
    ui = form_data.get("ui")
    video_opts = form_data.get("video-opts")

    data = [url, ui, video_opts]
    data = [None if isinstance(value, UploadFile) else value for value in data]

    url, ui, video_opts = data

    if not video_opts:
        video_opts = "none-selected"

    options = {"video-options": video_opts}

    if not url:
        log.error("No URL provided.")

        if not ui:
            return JSONResponse(
                {"success": False, "error": "/q called without a 'url' in form data"}
            )

        return RedirectResponse(url="/gallery-dl", status_code=HTTP_303_SEE_OTHER)

    task = BackgroundTask(download_task, url.strip(), options)

    log.info("Added URL to the download queue: %s", url)

    if not ui:
        return JSONResponse({"success": True, "url": url, "options": options}, background=task)

    return RedirectResponse(
        url="/gallery-dl?added=" + url, status_code=HTTP_303_SEE_OTHER, background=task
    )


def download_task(url: str, options: dict[str, str]):
    """Initiate download as a subprocess and log output."""
    log_queue = multiprocessing.Queue()
    return_status = multiprocessing.Queue()

    process = multiprocessing.Process(
        target=download.run, args=(url, options, log_queue, return_status)
    )
    process.start()

    while True:
        if log_queue.empty() and not process.is_alive():
            break

        try:
            record_dict = log_queue.get(timeout=1)
            record = output.dict_to_record(record_dict)

            if record.levelno >= log.getEffectiveLevel():
                log.handle(record)

            if "Video should already be available" in record.getMessage():
                log.warning("Terminating process as video is not available")
                process.kill()
        except queue.Empty:
            continue

    process.join()

    try:
        exit_code = return_status.get(block=False)
    except queue.Empty:
        exit_code = process.exitcode

    if exit_code == 0:
        log.info("Download process exited successfully")
    else:
        log.error("Download failed with exit code: %s", exit_code)


async def log_route(request: Request):
    async def read_log_file(file_path: str):
        log_contents = ""
        try:
            async with aiofiles.open(file_path, mode="r", encoding="utf-8") as file:
                async for line in file:
                    log_contents += line
        except FileNotFoundError:
            return "Log file does not exist."
        except Exception as e:
            log.debug(f"Exception: {type(e).__name__}: {e}")
            return f"An error occurred: {e}"

        return log_contents

    logs = await read_log_file(log_file)

    return templates.TemplateResponse(
        "logs.html", {"request": request, "app_version": version.__version__, "logs": logs}
    )


async def log_stream(request: Request):
    async def file_iterator(file_path: str):
        try:
            async with aiofiles.open(file_path, mode="r", encoding="utf-8") as file:
                while True:
                    chunk = await file.read(64 * 1024)
                    if not chunk:
                        break
                    if utils.WINDOWS:
                        yield chunk.replace("\n", "\r\n")
                    else:
                        yield chunk
        except FileNotFoundError:
            yield "Log file does not exist."
        except Exception as e:
            log.debug(f"Exception: {type(e).__name__}: {e}")
            yield f"An error occurred: {type(e).__name__}: {e}"

    return StreamingResponse(file_iterator(log_file), media_type="text/plain")


async def log_update(websocket: WebSocket):
    await websocket.accept()
    log.debug(f"Accepted WebSocket connection: {websocket}")

    async with connections_lock:
        active_connections.add(websocket)
        log.debug("WebSocket added to active connections")
    try:
        async with aiofiles.open(log_file, mode="r", encoding="utf-8") as file:
            await file.seek(0, os.SEEK_END)
            last_position = await file.tell()
            last_line = ""

            async for changes in watchfiles.awatch(log_file, stop_event=shutdown_event):
                await asyncio.sleep(1)
                await file.seek(last_position)

                new_content = ""
                previous_line = await output.read_previous_line(log_file)
                if previous_line and last_line:
                    if "B/s" in previous_line and "B/s" in last_line:
                        new_content = previous_line + "\n"

                new_content += await file.read()
                if new_content.strip():
                    await websocket.send_text(new_content)

                last_position = await file.tell()
                last_line = previous_line
    except asyncio.CancelledError as e:
        log.debug(f"Exception: {type(e).__name__}")
    except WebSocketDisconnect as e:
        log.debug(f"Exception: {type(e).__name__}")
    except Exception as e:
        log.debug(f"Exception: {type(e).__name__}: {e}")
    finally:
        async with connections_lock:
            if websocket in active_connections:
                active_connections.remove(websocket)
                log.debug("WebSocket removed from active connections")


@asynccontextmanager
async def lifespan(app: Starlette):
    uvicorn_log = output.configure_uvicorn_logs()
    uvicorn_log.info(f"Starting {type(app).__name__} application.")
    await shutdown_override()
    try:
        yield
    except asyncio.CancelledError as e:
        log.debug(f"Exception: {type(e).__name__}")
    finally:
        if utils.CONTAINER and os.path.isdir("/config"):
            if os.path.isfile(log_file) and os.path.getsize(log_file) > 0:
                dst_dir = "/config/logs"

                os.makedirs(dst_dir, exist_ok=True)

                dst = os.path.join(dst_dir, "app_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".log")
                shutil.copy2(log_file, dst)


async def shutdown_override():
    """Override uvicorn exit handler to ensure a graceful shutdown."""
    sigint_handler = signal.getsignal(signal.SIGINT)
    sigterm_handler = signal.getsignal(signal.SIGTERM)

    def shutdown(sig: int, frame: FrameType | None = None):
        shutdown_handler()

        if sig == signal.SIGINT and callable(sigint_handler):
            sigint_handler(sig, frame)
        elif sig == signal.SIGTERM and callable(sigterm_handler):
            sigterm_handler(sig, frame)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)


def shutdown_handler():
    """Initiate server shutdown."""
    if not shutdown_event.is_set():
        shutdown_event.set()
        log.debug("Set shutdown event")

    asyncio.create_task(close_connections())
    asyncio.create_task(output.close_handlers())


async def close_connections():
    """Close WebSocket connections and clear the set of active connections."""
    async with connections_lock:
        log.debug(f"Active connections before closing: {len(active_connections)}")
        log.debug(f"Active tasks before closing: {len(asyncio.all_tasks())}")

        close_connections = []
        for websocket in active_connections:
            if websocket.client_state == WebSocketState.CONNECTED:
                close_connections.append(websocket.close())
                log.debug(f"Scheduled WebSocket for closure: {websocket}")

        if close_connections:
            await asyncio.gather(*close_connections)
            log.debug("Closed all WebSocket connections")

        if active_connections:
            active_connections.clear()
            log.debug("Cleared active connections")


class CSPMiddleware(BaseHTTPMiddleware):
    """Enforce Content Security Policy for all requests."""

    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self';"
            "connect-src 'self';"
            "form-action 'self';"
            "manifest-src 'self';"
            "img-src 'self' data:;"
            "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net;"
            "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net https://fonts.googleapis.com;"
            "font-src 'self' https://cdnjs.cloudflare.com https://fonts.googleapis.com https://fonts.gstatic.com;"
        )
        return response


templates = Jinja2Templates(directory=utils.resource_path("templates"))

active_connections: set[WebSocket] = set()
connections_lock = asyncio.Lock()
shutdown_event = asyncio.Event()

routes = [
    Route("/", endpoint=redirect, methods=["GET"]),
    Route("/gallery-dl", endpoint=homepage, methods=["GET"]),
    Route("/gallery-dl/q", endpoint=submit_form, methods=["POST"]),
    Route("/gallery-dl/logs", endpoint=log_route, methods=["GET"]),
    Route("/stream/logs", endpoint=log_stream, methods=["GET"]),
    WebSocketRoute("/ws/logs", endpoint=log_update),
    Mount("/static", app=StaticFiles(directory=utils.resource_path("static")), name="static"),
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET", "POST"]),
    Middleware(CSPMiddleware),
]

app = Starlette(debug=True, routes=routes, middleware=middleware, lifespan=lifespan)
