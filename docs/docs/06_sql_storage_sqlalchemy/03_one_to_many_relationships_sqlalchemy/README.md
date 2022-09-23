---
title: One-to-many relationships with SQLAlchemy
description: Model relationships let us easily retrieve information about a related model, without having to do SQL JOINs manually.
---

# One-to-many relationships with SQLAlchemy

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

## Updating our marshmallow schemas

Now that the models have these relationships, we can modify our marshmallow schemas so they will return some or all of the information about the related models.

We do this with the `Nested` marshmallow field.

:::caution
Something to be careful about is having schema A which has a nested schema B, which has a nested schema A.

This will lead to an infinite nesting, which is obviously never what you want!
:::

To avoid infinite nesting, we are renaming our schemas which _don't_ use nested fields to `Plain`, such as `PlainItemSchema` and `PlainStoreSchema`.

Then the schemas that _do_ use nesting can be called `ItemSchema` and `StoreSchema`, and they inherit from the plain schemas. This reduces duplication and prevents infinite nesting.

```python title="schemas.py"
from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
```