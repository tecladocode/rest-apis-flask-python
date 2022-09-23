---
title: How to add a login endpoint to the REST API
description: Learn how to add a login endpoint that returns a JWT to a REST API using Flask-Smorest and Flask-JWT-Extended.
---

# How to add a login endpoint to the REST API

Now that we've done registration, we can do log in! It's very similar.

Let's import `flask_jwt_extended.create_access_token` so that when we receive a valid username and password from the client, we can create a JWT and send it back:

```diff title="resources/user.py"
from flask.views import MethodView
from flask_smorest import Blueprint, abort
+from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256
```

Then let's create our `UserLogin` resource.

```python title="resources/user.py"
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200

        abort(401, message="Invalid credentials.")
```

Here you can see the when we call `create_access_token(identity=user.id)` we pass in the user's `id`. This is what gets stored (among other things) inside the JWT, so when the client sends the JWT back on every request, we can tell who the JWT belongs to.