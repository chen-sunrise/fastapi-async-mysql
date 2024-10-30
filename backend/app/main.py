import asyncio
import time

import uvloop
from fastapi import FastAPI, Request

from app.api import api_router
from app.core.config import settings

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = FastAPI()


@app.middleware("http")
async def add_global_http_process(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(api_router, prefix=settings.API_V1_STR)
