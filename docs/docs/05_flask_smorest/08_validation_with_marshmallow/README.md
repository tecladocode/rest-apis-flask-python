---
title: Validation with marshmallow
description: We can use the marshmallow library to validate request data from our API clients.
---

# Validation with marshmallow

Now that we've got our schemas written, let's use them to validate incoming data to our API.

With Flask-Smorest, this couldn't be easier!

Let's start with `resources/item.py`

## Validation in `resources/item.py`

At the top of the file, import the schemas:

```py
from schemas import ItemSchema, ItemUpdateSchema
```

We have two sets of data that may be incoming (in the JSON body of a request): new items and updating items.

So let's go to the `ItemList#post` method and make a couple changes!

First, let's get rid of the existing data validation. Delete the highlighted lines below:

```py
def post(self):
    # highlight-start
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
        )
    # highlight-end
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

Now, I know what you're thinking! What about `item_data`? Do we not need to keep that?

When we use `marshmallow` for validation with Flask-Smorest, it will inject the validated data into our method for us.

Look at these two highlighted lines:

```py
# highlight-start
@blp.arguments(ItemSchema)
def post(self, item_data):
    # highlight-end
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

Nice!

Plus, doing this also adds to your Swagger UI documentation.

Let's do the same when updating items:

```py
# highlight-start
@blp.arguments(ItemUpdateSchema)
def put(self, item_data, item_id):
    # highlight-end
    try:
        item = items[item_id]
        item |= item_data

        return item
    except KeyError:
        abort(404, message="Item not found.")
```

:::caution Order of parameters
Be careful here since we've now got `item_data` and `item_id`. The URL arguments come in at the end. The injected arguments are passed first, so `item_data` goes before `item_id` in our function signature.
:::

## Validation in `resources/store.py`

Now let's do the same in `store.py`!

At the top of the file, import the schema:

```py
from schemas import StoreSchema
```

When creating a store, we'll have this:

```py
@blp.arguments(StoreSchema)
def post(cls, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists.")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store

        return store
```