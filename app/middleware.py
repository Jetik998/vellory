# middleware.py
import time
from fastapi import Request

request_count = 0
response_times = []


async def add_process_time_header(request: Request, call_next):
    global request_count, response_times

    request_count += 1
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time
    response_times.append(process_time)

    if len(response_times) > 1000:
        response_times.pop(0)

    response.headers["X-Process-Time"] = str(process_time)
    return response
