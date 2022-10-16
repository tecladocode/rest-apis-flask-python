---
title: The User model and schema
description: Create the SQLAlchemy User model and marshmallow schema.
---

# The User model and schema

Just as we did with items, stores, and tags, let's create two classes for our users:

- The SQLAlchemy model, to interact with the database.
- The marshmallow schema, to deserialize data from clients and serialize it back to return data.

## The User SQLAlchemy model

```python title="models/user.py"
from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
```

Let's also add this class to `models/__init__.py` so it can then be imported by `app.py`:

```python title="models/__init__.py"
from models.user import UserModel
from models.item import ItemModel
from models.tag import TagModel
from models.store import StoreModel
from models.item_tags import ItemsTags
```

## The User marshmallow schema

```python title="schemas.py"
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
```