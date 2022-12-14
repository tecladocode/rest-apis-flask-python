---
title: Conclusion of this section
description: Review everything we've changed this section to add SQL storage with SQLAlchemy to our API.
---

# Conclusion of this section

Adding SQL storage to our app has required quite a few changes! Let's do a quick review.

## Installed SQLAlchemy and Flask-SQLAlchemy

```
pip install sqlalchemy flask-sqlalchemy
```

And

```text title="requirements.txt"
sqlalchemy
flask-sqlalchemy
```

## Created models

```python title="models/item.py"
from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)

    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )
    store = db.relationship("StoreModel", back_populates="items")
```

And

```python title="models/store.py"
from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")
```

## Updated resources to use SQLAlchemy

Previously we were using Python dictionaries as a database. Now we've swapped them out for using SQLAlchemy models by:

- Importing the models in our resource files
- Retrieving models from the database with `ModelClass.query.get_or_404(model_id)`.
- Updating models by changing attributes, or creating new model class instances, and then saving and committing with `db.session.add(model_instance)` and `db.session.commit()`.
- Deleting models with `db.session.delete(model_instance)` followed by `db.session.commit()`.

## Updated marshmallow schemas

Since now our models have relationships, that means that the schemas can have `Nested` fields.

The schemas that don't have `Nested` fields we've called "Plain" schemas, and those that do are named after the model they represent.

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
    store_id = fields.Int()


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
```

And that's it! Quite a few changes, but hopefully you're still with me.

In the following sections we'll be adding more functionality to our API, so stay tuned!