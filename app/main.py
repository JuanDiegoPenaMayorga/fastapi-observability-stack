from fastapi import FastAPI

app = FastAPI(title="fastapi-observability-stack")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
    