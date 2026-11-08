import time

from fastapi import FastAPI, HTTPException, Request, Response, status
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.metrics import ERRORS, LATENCY, REQUESTS
from app.schemas import Item, ItemCreate

app = FastAPI(title="fastapi-observability-stack")


# ---Metrics start---
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start

    route = request.scope.get("route")
    path = route.path if route else "no_route"
    method = request.method
    code = str(response.status_code)

    REQUESTS.labels(method, path, code).inc()
    LATENCY.labels(method, path).observe(elapsed)
    if response.status_code >= 400:
        ERRORS.labels(method, path, code).inc()
    return response


@app.get("/metrics")
def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


# ---Metrics end---

_items: dict[int, Item] = {}
_next_id = 1


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items")
def list_items() -> list[Item]:
    return list(_items.values())


@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(data: ItemCreate) -> Item:
    global _next_id
    item = Item(id=_next_id, **data.model_dump())
    _items[item.id] = item
    _next_id += 1
    return item


@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return _items[item_id]


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> None:
    if _items.pop(item_id, None) is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")


@app.put("/items/{item_id}")
def update_item(item_id: int, data: ItemCreate) -> Item:
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    item = Item(id=item_id, **data.model_dump())
    _items[item_id] = item
    return item
