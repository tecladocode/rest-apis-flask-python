---
title: "Data model improvements"
description: "Use dictionaries instead of lists for data storage, and store stores and items separately."
---

# Data model improvements

## Starting code from section 4

This is the "First REST API" project from Section 4:

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<div className="codeTabContainer">
<Tabs>
<TabItem value="app" label="app.py" default>

```py title="app.py"
from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            }
        ]
    }
]

@app.get("/store")  # http://127.0.0.1:5000/store
def get_stores():
    return {"stores": stores}


@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404


@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"message": "Store not found"}, 404


@app.get("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404
```

</TabItem>
<TabItem value="docker" label="Dockerfile">

```docker
FROM python:3.10
EXPOSE 5000
WORKDIR /app
RUN pip install flask
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]
```

</TabItem>
</Tabs>
</div>

## New files

:::tip Insomnia files
Remember to get the Insomnia files for this section or for all sections [here](/insomnia-files/)!

There are two Insomnia files for this section: one for lectures 1-5 (before adding Docker), and one for the other lectures (after adding Docker).
:::

Let's start off by creating a `requirements.txt` file with all our dependencies:

```txt title="requirements.txt"
flask
flask-smorest
python-dotenv
```

We're adding `flask-smorest` to help us write REST APIs more easily, and generate documentation for us.

We're adding `python-dotenv` so it's easier for us to load environment variables and use the `.flaskenv` file.

Next, let's create the `.flaskenv` file:

```txt title=".flaskenv"
FLASK_APP=app
FLASK_DEBUG=True
```

If we have the `python-dotenv` library installed, when we run the `flask run` command, Flask will read the variables inside `.flaskenv` and use them to configure the Flask app.

The configuration that we'll do is to define the Flask app file (here, `app.py`). Then we'll also set the `FLASK_DEBUG` flag to `True`, which does a couple things:

- Makes the app give us better error messages and return a traceback when we make requests if there's an error.
- Sets the app reloading to true, so the app restarts when we make code changes

We don't want debug mode to be enabled in production (when we deploy our app), but while we're doing development it's definitely a time-saving tool!

## Code improvements

### Creating a database file

First of all, let's move our "database" to another file.

Create a `db.py` file with the following content:

```py title="db.py"
stores = {}
items = {}
```

In the existing code we only have a `stores` list, so delete that from `app.py`. From now on we will be storing information about items and stores separately.

:::tip What is in each dictionary?
Each dictionary will closely mimic how a database works: a mapping of ID to data. So each dictionary will be something like this:

```py
{
    1: {
        "name": "Chair",
        "price": 17.99
    },
    2: {
        "name": "Table",
        "price": 180.50
    }
}
```

This will make it much easier to retrieve a specific store or item, just by knowing its ID.
:::

Then, import the `stores` and `items` variables from `db.py` in `app.py`:

```py title="app.py"
from db import stores, items
```

## Using stores and items in our API

Now let's make use of stores and items separately in our API.

### `get_store`

Here are the changes we'll need to make:

<div className="codeTabContainer">
<Tabs>
<TabItem value="old" label="get_store (old)" default>

```py title="app.py"
@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"message": "Store not found"}, 404
```

</TabItem>
<TabItem value="new" label="get_store (new)">

```py title="app.py"
@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        # Here you might also want to add the items in this store
        # We'll do that later on in the course
        return stores[store_id]
    except KeyError:
        return {"message": "Store not found"}, 404
```

Important to note that in this version, we won't return the items in the store. That's a limitation of our dictionaries-for-database setup that we will solve when we introduce databases!

</TabItem>
</Tabs>
</div>

### `get_stores`

<div className="codeTabContainer">
<Tabs>
<TabItem value="old" label="get_stores (old)" default>

```py title="app.py"
@app.get("/store")
def get_stores():
    return {"stores": stores}
```

</TabItem>
<TabItem value="new" label="get_stores (new)">

```py title="app.py"
@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}
```

</TabItem>
</Tabs>
</div>

### `create_store`

<div className="codeTabContainer">
<Tabs>
<TabItem value="old" label="create_store (old)" default>

```py title="app.py"
@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201
```

</TabItem>
<TabItem value="new" label="create_store (new)">

```py title="app.py"
import uuid

@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store

    return store
```

Here we add a new import, [the `uuid` module](https://docs.python.org/3/library/uuid.html). We will be using it to create unique IDs for our stores and items instead of relying on the uniqueness of their names.

</TabItem>
</Tabs>
</div>

### `create_item`

<div className="codeTabContainer">
<Tabs>
<TabItem value="old" label="create_item (old)" default>

```py title="app.py"
@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404
```

</TabItem>
<TabItem value="new" label="create_item (new)">

```py title="app.py"
@app.post("/item")
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item
```

Now we are POSTing to `/item` instead of `/store/<string:name>/item`. The endpoint will expect to receive JSON with `price`, `name`, and `store_id`.

</TabItem>
</Tabs>
</div>


### `get_items` (new)

This is not an endpoint we could easily make when we were working with a single `stores` list!

```py
@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}
```

### `get_item_in_store`

<div className="codeTabContainer">
<Tabs>
<TabItem value="old" label="get_item_in_store (old)" default>

```py title="app.py"
@app.get("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404
```

</TabItem>
<TabItem value="new" label="get_item (new)">

```py title="app.py"
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Item not found"}, 404
```

Now we are GETting from `/item` instead of `/store/<string:name>/item`. This is because while items are related to stores, they aren't inside a store anymore!

</TabItem>
</Tabs>
</div>
