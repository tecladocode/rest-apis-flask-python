---
title: Decorating responses with Flask-Smorest
description: Add response serialization and status code to API endpoints, and add to your documentation in the process.
---

# Decorating responses with Flask-Smorest

We can use marshmallow schemas for serialization when we respond to a client. To do so, we need to tell Flask-Smorest what Schema to use when responding.

This will do a few things:

1. Update your documentation to show what data and status code will be returned by the endpoint.
2. Pass any data your endpoint returns through the marshmallow schema, casting data types and removing data that isn't in the schema.

## Decorating responses in `resources/item.py`

Let's start with retrieving a specific item.

Up until now, we've been doing this:

```py
def get(self, item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")
```

But now we can run the `items[item_id]` dictionary through the marshmallow schema and tell Flask-Smorest about it so the documentation will be updated:

```py
@blp.response(200, ItemSchema)
def get(self, item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")
```

:::info
The number, `200`, is the status code. It means "OK" (all good).
:::

Our endpoint for updating items looks like this:

```py
@blp.arguments(ItemUpdateSchema)
def put(self, item_data, item_id):
    try:
        item = items[item_id]
        item |= item_data

        return item
    except KeyError:
        abort(404, message="Item not found.")
```

Let's pass this through the schema as well:

```py
@blp.arguments(ItemUpdateSchema)
# highlight-start
@blp.response(200, ItemSchema)
# highlight-end
def put(self, item_data, item_id):
    try:
        item = items[item_id]

        # https://blog.teclado.com/python-dictionary-merge-update-operators/
        item |= item_data

        return item
    except KeyError:
        abort(404, message="Item not found.")
```

:::caution
Careful with the order of decorators in these functions!
:::

When we get to returning a list of items, it looks like this:

```py
# highlight-start
@blp.response(200, ItemSchema(many=True))
# highlight-end
def get(self):
    return items.values()
```

And finally, don't forget to decorate the new item endpoint too:

```py
@blp.arguments(ItemSchema)
# highlight-start
@blp.response(201, ItemSchema)
# highlight-end
def post(self, item_data):
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message=f"Item already exists.")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item
```

## Decorating responses in `resources/store.py`

Going a bit more quickly here since you already know what's going on with this decorator. The highlighted lines are new:

```py title="resources/store.py"
import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema


blp = Blueprint("Stores", "stores", description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    # highlight-start
    @blp.response(200, StoreSchema)
    # highlight-end
    def get(cls, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")

    def delete(cls, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):
    # highlight-start
    @blp.response(200, StoreSchema(many=True))
    # highlight-end
    def get(cls):
        return stores.values()

    @blp.arguments(StoreSchema)
    # highlight-start
    @blp.response(201, StoreSchema)
    # highlight-end
    def post(cls, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists.")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store

        return store
```