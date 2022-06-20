---
title: Change SQLAlchemy models and generate a migration
description: Use Flask-Migrate to generate a new database migration after changing your SQLAlchemy models.
---

# Change SQLAlchemy models and generate a migration

Let's make a change to one of our SQLAlchemy models and then generate another migration script. This is what we will do every time we want to make changes to our models and our database schema.

```python title="models/item.py"
from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    # highlight-start
    description = db.Column(db.String)
    # highlight-end
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)

    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )
    store = db.relationship("StoreModel", back_populates="items")

    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
```

Here we're adding a simple column, just a string that doesn't have any constraints.

Now let's go to the terminal and run the command:

```
flask db migrate
```

This will now generate _another migration script_ that you have to double-check. Make sure to check the upgrade and downgrade functions.

When you're happy with the contents, apply the migration:

```
flask db upgrade
```