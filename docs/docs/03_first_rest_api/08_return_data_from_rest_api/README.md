---
title: Get a specific store and its items
description: How to use Flask to return data from your REST API to your client.
---

# How to get a specific store and its items

The last thing we want to look at in our first REST API is returning data that uses some filtering.

Using URL parameters, we can select a specific store:

```py
@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"message": "Store not found"}, 404
```

And just as we did when creating an item in a store, you can use the same endpoint (with a `GET` method), to select the items in a store:

```py
@app.get("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404
```
