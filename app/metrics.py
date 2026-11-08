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
)
