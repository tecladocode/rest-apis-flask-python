---
title: How to add a register endpoint to the REST API
description: Learn how to add a registration endpoint to a REST API using Flask-Smorest and Flask-JWT-Extended.
---

# How to add a register endpoint to the REST API

Registering users sounds like a conceptually very difficult thing, but let's break it down into steps:

- Receive username and password from the client (as JSON).
- Check if a user with that username already exists.
- If it doesn't...
  - Encrypt the password.
  - Add a new `UserModel` to the database.
  - Return a success message.

## Boilerplate set-up for a blueprint with Flask-Smorest

First, we need our imports and blueprint set-up. This is the same for pretty much every Flask-Smorest blueprint, so you already know how to do it!

```python title="resources/user.py"
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

from db import db
from models import UserModel
from schemas import UserSchema


blp = Blueprint("Users", "users", description="Operations on users")
```

## Creating the `UserRegister` resource

Now let's create the `MethodView` class, and register a route to it using the blueprint:

```python title="resources/user.py"
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

from db import db
from models import UserModel
from schemas import UserSchema


blp = Blueprint("Users", "users", description="Operations on users")


# highlight-start
@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201
# highlight-end
```

## Creating a testing-only `User` resource

Let's also create a `User` resource that we will only use during testing. It allows us to retrieve information about a single user, or delete a user. This will be handy so that using Insomnia or Postman we can clear the registered users and we don't have to change our request arguments each time!

```python title="resources/user.py"
@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
```

## Register the user blueprint in `app.py`

Finally, let's go to `app.py` and register the blueprint!

```diff title="app.py"
+from resources.user import blp as UserBlueprint
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint

...

+api.register_blueprint(UserBlueprint)
api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)
api.register_blueprint(TagBlueprint)
```