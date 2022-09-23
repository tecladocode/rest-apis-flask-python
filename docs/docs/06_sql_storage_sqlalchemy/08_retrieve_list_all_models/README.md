---
title: Retrieve a list of all models
description: Get more than one model and return it as a list from the API.
---

# Retrieve a list of all models

Using the `query` attribute of our model class, we can retrieve all the results of the query:

```python title="resources/item.py"
@blp.response(200, ItemSchema(many=True))
def get(self):
    # highlight-start
    return ItemModel.query.all()
    # highlight-end
```

```python title="resources/store.py"
@blp.response(200, StoreSchema(many=True))
def get(self):
    # highlight-start
    return StoreModel.query.all()
    # highlight-end
```