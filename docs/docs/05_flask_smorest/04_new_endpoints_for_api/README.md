---
title: "New endpoints for our REST API"
description: "Let's add a few routes to our first REST API, so it better matches what a production REST API would look like."
---

# New endpoints for our REST API

## New endpoints

We want to add some endpoints for added functionality:

- `DELETE /item/<string:item_id>` so we can delete items from the database.
- `PUT /item/<string:item_id>` so we can update items.
- `DELETE /store/<string:store_id>` so we can delete stores.

### Deleting items

This is almost identical to getting items, but we use the `del` keyword to remove the entry from the dictionary.

```py title="app.py"
@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found.")
```

### Updating items

This is almost identical to creating items, but in this API we've decided to not let item updates change the `store_id` of the item. So clients can change item name and price, but not the store that the item belongs to.

This is an API design decision, and you could very well allow clients to update the `store_id` if you want!

```py title="app.py"
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    # There's  more validation to do here!
    # Like making sure price is a number, and also both items are optional
    # You should also prevent keys that aren't 'price' or 'name' to be passed
    # Difficult to do with an if statement...
    if "price" not in item_data or "name" not in item_data:
        abort(
            400,
            message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
        )
    try:
        item = items[item_id]
        item |= item_data

        return item
    except KeyError:
        abort(404, message="Item not found.")
```

:::tip Dictionary update operators
The `|=` syntax is a new dictionary operator. You can read more about it [here](https://blog.teclado.com/python-dictionary-merge-update-operators/).
:::

### Deleting stores

This is very similar to deleting items!

```py title="app.py"
@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not found.")
```
