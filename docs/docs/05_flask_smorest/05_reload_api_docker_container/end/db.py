"""
db.py
---

Later on, this file will be replaced by SQLAlchemy. For now, it mimics a database.
Our data storage is:
    - stores have a unique ID and a name
    - items have a unique ID, a name, a price, and a store ID.
"""

stores = {}
items = {}
