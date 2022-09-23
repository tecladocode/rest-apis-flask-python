---
title: Get models by ID from the database
description: Learn how to fetch a specific model using its primary key column, and how to return a 404 page if it isn't found.
---

# Get models by ID from the database using SQLAlchemy

Using the model class's `query` attribute, we have access to two very handy methods:

- `ItemModel.query.get(item_id)` gives us an `ItemModel` object from the database where the `item_id` matches the primary key.
- `ItemModel.query.get_or_404(item_id)` does the same, but makes Flask immediately return a "Not Found" message, together with a 404 error code, if no model can be found with that ID in the database.

:::tip
When we use `.get_or_404()` and nothing is found, this is the response from the API:

```json
{"code": 404, "status": "Not Found"}
```

The status code of this response is also 404.
:::

We're going to use `.get_or_404()` repeatedly in our resources!

For now, and since we'll need an `ItemModel` instance in all our `Item` resource methods, let's add that:

```python title="resources/item.py"
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        # highlight-start
        item = ItemModel.query.get_or_404(item_id)
        return item
        # highlight-end

    def delete(self, item_id):
        # highlight-start
        item = ItemModel.query.get_or_404(item_id)
        # highlight-end
        raise NotImplementedError("Deleting an item is not implemented.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        # highlight-start
        item = ItemModel.query.get_or_404(item_id)
        # highlight-end
        raise NotImplementedError("Updating an item is not implemented.")
```

Similarly in our `Store` resource:

```python title="resources/store.py"
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        # highlight-start
        store = StoreModel.query.get_or_404(store_id)
        return store
        # highlight-end

    def delete(self, store_id):
        # highlight-start
        store = StoreModel.query.get_or_404(store_id)
        # highlight-end
        raise NotImplementedError("Deleting a store is not implemented.")
```

With this, we're ready to continue!