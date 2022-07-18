from typing import Union

from fastapi import FastAPI
base_url = '/api/'
app = FastAPI()


@app.get("/api/")
def read_root():
    return {"Hello": "Warld"}


@app.get("/api/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}