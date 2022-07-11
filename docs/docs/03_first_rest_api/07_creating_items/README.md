---
title: How to create items in each store
description: A brief description of the lecture goes here.
---

# How to create items in our REST API

Next up, let's work on adding items to a store!

Here's how that's going to work:

1. The client will send us the store name where they want their new item to go.
2. They will also send us the name and price of the new item.
3. We'll go through the stores one at a time, until we find the correct one (whose name matches what the user gave us).
4. We'll append a new item dictionary to that store's `items`.

## URL parameters

There are a few ways for clients to send us data. So far, we've seen that clients can send us JSON.

But data can be included in a few other places:

- The body (as JSON, form data, plain text, or a variety of other formats).
- Inside the URL, part of it can be dynamic.
- At the end of the URL, as _query string arguments_.
- In the request headers.

For this request, the client will send us data in two of these at the same time: the body and the URL.

How does a dynamic URL look like?

Here's a couple examples:

- `/store/My Store/item`
- `/store/another-store/item`
- `/store/a/item`

In those three URLs, the "store name" was:

- `My Store`
- `another-store`
- `a`

We can use Flask to define dynamic endpoints for our routes, and then we can grab the value that the client put inside the URL.

This allows us to make URLs that make interacting with them more natural.

For example, it's nicer to make an item by going to `POST /store/My Store/item`, rather than going to `POST /add-item` and then pass in the store name in the JSON body.

To create a dynamic endpoint for our route, we do this:

```py
@app.route("/store/<string:name>/item")
```

That makes it so the route function will use a `name` parameter whose value will be what the client put in that part of the URL.

Without further ado, let's make our route for creating items within a store!

```py title="app.py"
from flask import Flask, request

app = Flask(__name__)

stores = [{"name": "My Store", "items": [{"name": "my item", "price": 15.99}]}]


@app.get("/store")
def get_stores():
    return {"stores": stores}


@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


# highlight-start
@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item
    return {"message": "Store not found"}, 404
# highlight-end
```

:::tip Not the most efficient way
In this endpoint we're iterating over all stores in our list until we find the right one. This is very inefficient, but we'll look at better ways to do this kind of thing when we look at databases.

For now, focus on Flask, and don't worry about efficiency of our code!
:::