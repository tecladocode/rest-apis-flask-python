---
title: Delete models with SQLAlchemy
description: Use SQLAlchemy to handle removal of a specific model.
---

# Delete models with SQLAlchemy

Just as with adding, deleting models is a matter of using `db.session`, and then committing when the deletion is complete:

```python title="resources/item.py"
def delete(self, item_id):
    item = ItemModel.query.get_or_404(item_id)
    # highlight-start
    db.session.delete(item)
    db.session.commit()
    return {"message": "Item deleted."}
    # highlight-end
```

```python title="resources/store.py"
def delete(self, store_id):
    store = StoreModel.query.get_or_404(store_id)
    # highlight-start
    db.session.delete(store)
    db.session.commit()
    return {"message": "Store deleted"}, 200
    # highlight-end
```