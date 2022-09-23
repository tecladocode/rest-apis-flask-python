---
title: Protect endpoints by requiring a JWT
description: Use jwt_required from Flask-JWT-Extended to prevent unauthorised users from making requests to certain endpoints in a REST API.
---

# Protect endpoints by requiring a JWT

Now that our users can sign up and log in, that means we can start _requiring login_ for certain endpoints.

All this means in practice is that the client making the request must send a valid JWT.

Remember, we can tell if a JWT is valid because it is _signed by our app_. If the user changes the JWT at all, the signature will be invalid, and we'll know it has been tampered with. Flask-JWT-Extended takes care of all that for us.

## Protecting routes in the `Item` resource

```python title="resources/item.py"
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# highlight-start
from flask_jwt_extended import jwt_required
# highlight-end
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", "items", description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    # highlight-start
    @jwt_required()
    # highlight-end
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    # highlight-start
    @jwt_required()
    # highlight-end
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(**item_data)

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    # highlight-start
    @jwt_required()
    # highlight-end
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    # highlight-start
    @jwt_required()
    # highlight-end
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

## Error handling with Flask-JWT-Extended

There are many things that could go wrong with JWTs:

- The JWT may be expired (they don't last forever!)
- The JWT may be invalid, such as if the client makes changes to it
- A JWT may be required, but none was provided
- There's more (we'll look at them in coming lectures!)

Let's go to `app.py` and add some configuration to tell Flask-JWT-Extended what to do in each of these cases.

At the top, let's import `jsonify`:

```python title="app.py"
from flask import Flask, jsonify
```

Then, after we define the `jwt = JWTManager(app)` variable, we can write some functions, each of which can run in different problem scenarios.

```python title="app.py"
...

app.config["JWT_SECRET_KEY"] = "jose"
jwt = JWTManager(app)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )

...
```

:::tip
Note that some Flask-JWT-Extended error functions take two arguments: `jwt_header` and `jwt_payload`. Others take a single argument, `error`.

The ones that don't take JWT information are those that would be called when a JWT is not present (above, when the JWT is invalid or required but not received).
:::