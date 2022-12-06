---
title: Delete models with relationships
description: Tell SQLAlchemy what to do with related models when you delete the parent.
---

# Delete models with relationships using cascades

When you delete a model that has a relationship to other models that still exist, the default behavior in SQLAlchemy with PostgreSQL is to raise an error. This is because SQLAlchemy does not want to allow you to accidentally delete data that is still being used by other models.

Let's say you have a `Store 1` that has two items, `Item 1` and `Item 2`. If you try to delete Store 1 without first deleting Item 1 and Item 2, SQLAlchemy will raise an error because the items are still related to the store.

This means the items have a **Foreign Key** that references the store you're trying to delete. If the store actually was deleted, the items have a store ID that references something that doesn't exist.

To fix this, you can use a feature called "cascading deletes". Cascading deletes allow you to specify that when a model is deleted, any related models should also be deleted automatically.

SQLAlchemy makes it easy to add cascades to our models, here's how you might do that!

```python title="models/store.py"
from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    # highlight-start
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")
    # highlight-end
```

Remember that `StoreModel` and `ItemModel` have a one-to-many relationship, where each store can have multiple items, and each item belongs to a single store.

The `cascade="all,delete"` argument in the `relationship()` call for the `StoreModel.items` attribute specifies that when a store is deleted, all of its related items should also be deleted.

If you add a `cascade` on the relationship in the `ItemModel`, then when an item is deleted, its related store should also be deleted. This is not what we want, so we won't add a cascade to `ItemModel`.

With this code in place, if you try to delete a store that still has items, the items will be deleted automatically along with the store. This will allow you to delete the store without having to delete the items individually.

For more information, I strongly recommend reading [the official documentation](https://docs.sqlalchemy.org/en/20/orm/cascades.html#delete)! There are also other cascade options you can pass in depending on what you want to happen to related models when the parent changes or is deleted.