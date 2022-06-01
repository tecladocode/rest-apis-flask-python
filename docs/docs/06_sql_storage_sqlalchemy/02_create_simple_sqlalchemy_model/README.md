---
title: Create a simple SQLAlchemy Model
description: Lecture description goes here.
---

# Create a simple SQLAlchemy Model

## Initialize the SQLAlchemy instance

```python title="db.py"
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

## Create models without relationships

Every model inherits from `db.Model`. That way when we tell SQLAlchemy about them (in [Configure Flask-SQLAlchemy](../configure_flask_sqlalchemy))), it will know to look at them to create tables.

Every model also has a few properties that let us interact with the database through the model, such as `query` (more on this in [Insert models in the database with SQLAlchemy](../insert_models_sqlalchemy)).

```python title="models/item.py"
from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, unique=False, nullable=False)
```

```python title="models/store.py"
from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
```