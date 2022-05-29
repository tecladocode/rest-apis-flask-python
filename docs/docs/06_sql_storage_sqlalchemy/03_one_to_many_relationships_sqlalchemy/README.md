---
title: One-to-many relationships with SQLAlchemy
description: Model relationships let us easily retrieve information about a related model, without having to do SQL JOINs manually.
---

# One-to-many relationships with SQLAlchemy

- [x] Set metadata above
- [x] Start writing!
- [x] Create `start` folder
- [x] Create `end` folder
- [ ] Create per-file diff between `end` and `start` (use "Compare Folders")

```python title="models/item.py"
from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)

    # highlight-start
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )
    store = db.relationship("StoreModel", back_populates="items")
    # highlight-end
```

```python title="models/store.py"
from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    # highlight-start
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")
    # highlight-end
```

To make it easier to import and use the models, I'll also create a `models/__init__.py` file that imports the models from their files:

```python title="models/__init__.py"
from models.store import StoreModel
from models.item import ItemModel
```

## What is `lazy="dynamic"`?

Without `lazy="dynamic"`, the `items` attribute of the `StoreModel` resolves to a list of `ItemModel` objects.

With `lazy="dynamic"`, the `items` attribute resolves to a SQLAlchemy **query**, which has some benefits and drawbacks:

- A key benefit is load speed. Because SQLAlchemy doesn't have to go to the `items` table and load items, stores will load faster.
- A key drawback is accessing the `items` of a store isn't as easy.
  - However this has another hidden benefit, which is that when you _do_ load items, you can do things like filtering before loading.

Here's how you could get all the items, giving you a list of `ItemModel` objects. Assume `store` is a `StoreModel` instance:

```python
store.items.all()
```

And here's how you would do some filtering:

```python
store.items.filter_by(name=="Chair").first()
```