import uuid
from flask import Flask, request

app = Flask(__name__)

stores = {}
items = {}


@app.get("/item/<string:id>")
def get_item(id):
    try:
        return items[id]
    except KeyError:
        return {"message": "Item not found"}, 404


@app.post("/items")
def create_item():
    request_data = request.get_json()
    new_item_id = uuid.uuid4().hex
    new_item = {
        "name": request_data["name"],
        "price": request_data["price"],
        "store_id": request_data["store_id"],
    }
    items[new_item_id] = new_item
    return new_item


@app.get("/items")
def get_all_items():
    return {"items": list(items.value())}


@app.get("/stores/<string:id>")
def get_store(id):
    try:
        # Here you might also want to add the items in this store
        # We'll do that later on in the course
        return stores[id]
    except KeyError:
        return {"message": "Store not found"}, 404


@app.post("/stores")
def create_store():
    request_data = request.get_json()
    new_store_id = uuid.uuid4().hex
    new_store = {"id": new_store_id, "name": request_data["name"]}
    stores[new_store_id] = new_store
    return new_store, 201


@app.get("/stores")
def get_all_stores():
    return {"stores": list(stores.value())}
