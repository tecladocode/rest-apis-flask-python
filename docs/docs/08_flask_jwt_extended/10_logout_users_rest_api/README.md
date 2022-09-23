---
title: How to add logout to the REST API
description: Create a logout endpoint that blocks certain JWTs from making further authenticated requests.
---

# How to add logout to the REST API

To log an user out we must _revoke_ their JWT. That way, if they send us the same JWT again, we can check whether it's been revoked or not. If it has, then we won't authorize them.

To do this, we need a central store of revoked JWTs that we keep around at least until the revoked JWT has expired.

Let's create our central revoked JWT storage in a file called `blocklist.py`. You could store this in the database instead, if you prefer. I'll leave that as an exercise for you.

```python title="blocklist.py"
"""
blocklist.py

This file just contains the blocklist of the JWT tokens. It will be imported by
app and the logout resource so that tokens can be added to the blocklist when the
user logs out.
"""

BLOCKLIST = set()
```

## Flask-JWT-Extended blocklist configuration for user logout

Now, in `app.py`, let's add some more Flask-JWT-Extended configuration to do two things:

- Check whether any JWT received is in the blocklist.
- If they are, return an error message to that effect.

```python title="app.py"
from blocklist import BLOCKLIST

...

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )
```

## How to perform logout (i.e. add JWTs to the blocklist)

Finally we need a resource in `resources/user.py` to actually add the user's JWT to the blocklist when they log out.

```python title="resources/user.py"
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    # highlight-start
    get_jwt,
    jwt_required,
    # highlight-end
)
from passlib.hash import pbkdf2_sha256

from db import db
from models import UserModel
from schemas import UserSchema
# highlight-start
from blocklist import BLOCKLIST
# highlight-end


blp = Blueprint("Users", "users", description="Operations on users")

# highlight-start
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200
# highlight-end


# Other User routes here
```