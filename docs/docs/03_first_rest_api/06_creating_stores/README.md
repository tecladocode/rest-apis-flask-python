---
title: How to create stores
description: Learn how to add data to our REST API.
---

# How to create stores in our REST API

To create a store, we'll receive JSON from our client (in our case, Insomnia, but it could be another Python app, JavaScript, or any other language or tool).

Our client will send us the name of the store they want to create, and we will add it to the database!

For this, we will use a `POST` method. `POST` is usually used to receive data from clients and either use it, or create resources with it.

In order to access the JSON body of a request, we will need to import `request` from `flask`. Your import list should now look like this:

```py
from flask import Flask, request
```

Then, create your endpoint:

```py title="app.py"
# highlight-start
from flask import Flask, request
# highlight-end

app = Flask(__name__)

stores = [{"name": "My Store", "items": [{"name": "my item", "price": 15.99}]}]


@app.get("/store")
def get_stores():
    return {"stores": stores}


# highlight-start
@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201
# highlight-end
```

Here we use `request.get_json()` to retrieve the JSON content of our request.

Then we create a new dictionary that represents our store. It has a `name` and `items` (which is an empty list).

Then we append this store to our `stores` list.

Finally we return the newly created `store`. It's empty, but it serves as a **success message**, to tell our client that we have successfully created what they wanted us to create.

:::tip Returning a status code
Every response has a status code, which tells the client if the server was successful or not. You already know at least one status code: 404. This means "Not found".

The most common status code is `200`, which means "OK". That's what Flask returns by default, such as in the `get_stores()` function.

If we want to return a different status code using Flask, we can put it as the second value returned by an endpoint function. In `create_store()`, we are returning the code `201`, which means "Created".
:::