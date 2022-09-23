---
title: Insert models in the database with SQLAlchemy
description: Learn how to use SQLAlchemy to add new rows to our SQL database.
---

# Insert models in the database with SQLAlchemy

Inserting models with SQLAlchemy couldn't be easier! We'll use the `db.session`[^1] variable to `.add()` a model. Let's begin working on our `Item` resource:

```python title="resources/item.py"
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel

...

@blp.arguments(ItemSchema)
@blp.response(201, ItemSchema)
def post(self, item_data):
    item = ItemModel(**item_data)

    try:
        db.session.add(item)
        db.session.commit()
    except SQLAlchemyError:
        abort(500, message="An error occurred while inserting the item.")

    return item
```

Similarly in our `Store` resource:

```python title="resources/store.py"
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel

...

@blp.arguments(StoreSchema)
@blp.response(201, StoreSchema)
def post(self, store_data):
    store = StoreModel(**store_data)
    try:
        db.session.add(store)
        db.session.commit()
    except IntegrityError:
        abort(
            400,
            message="A store with that name already exists.",
        )
    except SQLAlchemyError:
        abort(500, message="An error occurred creating the store.")

    return store
```

Note here we're catching two different errors, `IntegrityError` for when a client attempts to create a store with a name that already exists, and `SQLAlchemyError` for anything else.

Since the `StoreModel`'s `name` column is marked as `unique=True`, then an `IntegrityError` is raised when we try to insert another row with the same name.

[^1]: [Session Basics (SQLAlchemy Documentation)](https://docs.sqlalchemy.org/en/14/orm/session_basics.html)