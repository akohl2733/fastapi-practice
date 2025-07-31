from typing import Union, Annotated, Literal
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Field

app = FastAPI()

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_by", "updated_at"] = "created_by"
    tags: list[str] = []

class Item(BaseModel):
    name: str
    price: float = Field(default=0.0, validate_default=True)
    is_offer: Union[bool, None] = None

class GroceryList(BaseModel):
    items: list[Item] = []   

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="Item-query")] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
    

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item-price": item.price, "item_id": item_id}