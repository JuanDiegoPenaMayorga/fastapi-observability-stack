from fastapi import FastAPI, HTTPException, status

from app.schemas import Item, ItemCreate

app = FastAPI(title="fastapi-observability-stack")

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
