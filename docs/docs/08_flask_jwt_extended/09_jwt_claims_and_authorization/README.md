---
title: JWT claims and authorization
description: Learn how to add claims (extra info) to a JWT and use it for authorization in endpoints of a REST API.
---

# JWT Claims and Authorization

JWT claims are extra data we can add to the JWT. For example, we could store in the JWT whether the user whose ID is stored in the JWT is an "administrator" or not.

By doing this, we only have to check the user's permissions once, when we create the JWT, and not every time the user makes a request.

To add a custom claim to a JWT we define a function similar to the error handling functions we wrote in the last lecture:

```python title="app.py"
app.config["JWT_SECRET_KEY"] = "jose"
jwt = JWTManager(app)

# highlight-start
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}
# highlight-end

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )
```

:::caution Read from a database or config file
Here we're assuming that the user with and ID of `1` will be the administrator. Normally you'd read this from either a config file or the database.
:::

## How to use JWT claims in an endpoint

Let's make a small change to the `Item` resource so that only admins can delete items.

To do so, we'll need to add an import for `get_jwt`:

```python title="resources/item.py"
from flask_jwt_extended import jwt_required, get_jwt
```

Then in the `delete` endpoint, we can use `get_jwt()` to check the data in the JWT (which behaves like a dictionary):

```python title="resources/item.py"
@jwt_required()
def delete(self, item_id):
    # highlight-start
    jwt = get_jwt()
    if not jwt.get("is_admin"):
        abort(401, message="Admin privilege required.")
    # highlight-end

    item = ItemModel.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return {"message": "Item deleted."}
```