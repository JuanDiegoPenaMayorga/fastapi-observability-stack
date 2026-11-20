from prometheus_client import Counter, Histogram

REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "path", "status"],
)
ERRORS = Counter(
    "http_errors_total",
    "Total HTTP Errors (4xx and 5xx)",
    ["method", "path", "status"],
)
LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Duration in seconds",
    ["method", "path"],
    buckets=(
        0.0001,  # 0.1 ms
        0.00025, # 0.25 ms
        0.0005,  # 0.5 ms
        0.001,   # 1 ms
        0.0025,  # 2.5 ms
        0.005,   # 5 ms
        0.01,    # 10 ms
        0.025,   # 25 ms
        0.05,    # 50 ms
        0.1,     # 100 ms
        0.25,    # 250 ms
        0.5,     # 500 ms
        1.0,     # 1 s
    ),
)
