from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response
import time
import random

app = FastAPI()

REQUEST_COUNT = Counter(
    "recommendation_requests_total",
    "Total recommendation requests"
)

LATENCY = Histogram(
    "recommendation_latency_seconds",
    "Recommendation latency"
)

ERROR_COUNT = Counter(
    "recommendation_errors_total",
    "Recommendation errors"
)


@app.get("/recommend")
def recommend():
    REQUEST_COUNT.inc()

    with LATENCY.time():
        time.sleep(random.uniform(0.1, 1.0))

        if random.random() < 0.2:
            ERROR_COUNT.inc()
            return {"error": "model failure"}

    return {"posts": ["post1", "post2"]}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
