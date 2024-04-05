---
title: Updating models with SQLAlchemy
description: How to make changes to an existing model, or insert one if it doesn't already exist.
ctslug: updating-models-with-sqlalchemy
---

# Updating models with SQLAlchemy

A frequent operation in REST APIs is the "upsert", or "update or insert".

This is an idempotent operation where we send the data we want the API to store. If the data identifier already exists, an update is done. If it doesn't, it is created.

This idempotency is frequently seen with `PUT` requests. You can see it in action here:

```python title="resources/item.py"
@blp.arguments(ItemUpdateSchema)
@blp.response(200, ItemSchema)
def put(self, item_data, item_id):
    # highlight-start
    item = ItemModel.query.get(item_id)
    if item:
        item.price = item_data["price"]
        item.name = item_data["name"]
    else:
        item = ItemModel(id=item_id, **item_data)

    db.session.add(item)
    db.session.commit()

    return item
    # highlight-end
```

Our `ItemUpdateSchema` at the moment looks like this:

```python title="schemas.py"
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
```

But since now our update endpoint may create items, we need to change the schema to optionally accept a `store_id`.

When updating an item, `name` or `price` (or both) may be passed, but when creating an item, `name`, `price`, and `store_id` must be passed.

Update the `ItemUpdateSchema` to this:

```python title="schemas.py"
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()
```
