---
title: How to use Blueprints and MethodViews
description: Flask-Smorest MethodViews allow us to simplify API Resources by defining all methods that interact with the resource in one Python class.
---

# How to use Flask-Smorest MethodViews and Blueprints

Let's improve the structure of our code by splitting items and stores endpoints into their own files.

Let's create a `resources` folder, and inside it create `item.py` and `store.py`.

## Creating a blueprint for each related group of resources

### `resources/store.py`

Let's start in `store.py`, and create a `Blueprint`:

```py title="resources/store.py"
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores


blp = Blueprint("stores", __name__, description="Operations on stores")
```

The `Blueprint` arguments are the same as the Flask `Blueprint`[^1], with an added optional `description` keyword argument:

1. `"stores"` is the name of the blueprint. This will be shown in the documentation and is prepended to the endpoint names when you use `url_for` (we won't use it).
2. `__name__` is the "import name".
3. The `description` will be shown in the documentation UI.


Now that we've got this, let's add our `MethodView`s. These are classes where each method maps to one endpoint. The interesting thing is that method names are important:

```py title="resources/store.py"
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        pass

    def delete(self, store_id):
        pass
```

Two things are going on here:

1. The endpoint is associated to the `MethodView` class. Here, the class is called `Store` and the endpoint is `/store/<string:store_id>`.
2. There are two methods inside the `Store` class: `get` and `delete`. These are going to map directly to `GET /store/<string:store_id>` and `DELETE /store/<string:store_id>`.

Now we can copy the code from earlier into each of the methods:

```py title="resources/store.py"
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")
```

Now, still inside the same file, we can add another `MethodView` with a different endpoint, for the `/store` route:

```py title="resources/store.py"
@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}

    def post(self):
        store_data = request.get_json()
        if "name" not in store_data:
            abort(
                400,
                message="Bad request. Ensure 'name' is included in the JSON payload.",
            )
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists.")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store

        return store
```

### `resources/item.py`

Let's do the same thing with the `resources/item.py` file:

```py title="resources/item.py"
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items

blp = Blueprint("Items", "items", description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    def put(self, item_id):
        item_data = request.get_json()
        # There's  more validation to do here!
        # Like making sure price is a number, and also both items are optional
        # Difficult to do with an if statement...
        if "price" not in item_data or "name" not in item_data:
            abort(
                400,
                message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
            )
        try:
            item = items[item_id]

            # https://blog.teclado.com/python-dictionary-merge-update-operators/
            item |= item_data

            return item
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = request.get_json()
        # Here not only we need to validate data exists,
        # But also what type of data. Price should be a float,
        # for example.
        if (
            "price" not in item_data
            or "store_id" not in item_data
            or "name" not in item_data
        ):
            abort(
                400,
                message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
            )
        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message=f"Item already exists.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item
```

## Import blueprints and Flask-Smorest configuration

Finally, we have to import the `Blueprints` inside `app.py`, and register them with Flask-Smorest:

```py title="app.py"
from flask import Flask
from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint


app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)
```

I've also added a few config variables to the `app.config`. The `PROPAGATE_EXCEPTIONS` value is used so that when an exception is raised in an extension, it is bubbled up to the main Flask app so you'd see it more easily.

The other config values are there for the documentation of our API, and they define things such as the API name and version, as well as information for the Swagger UI.

Now you should be able to go to `http://127.0.0.1:5000/swagger-ui` and see your Swagger documentation rendered out!

[^1]: [Flask Blueprint (Flask Official Documentation)](https://flask.palletsprojects.com/en/2.1.x/api/#flask.Blueprint)