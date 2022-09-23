---
title: Updating models with SQLAlchemy
description: How to make changes to an existing model, or insert one if it doesn't already exist.
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
