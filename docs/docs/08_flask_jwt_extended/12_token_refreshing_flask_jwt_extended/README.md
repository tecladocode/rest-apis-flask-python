---
title: Token refreshing with Flask-JWT-Extended
description: Learn about fresh and non-fresh tokens, as well as how to use a refresh token to generate a new, non-fresh access token.
---

# Token refreshing with Flask-JWT-Extended

One of the problems with JWT authentication is that JWTs expire, and then the user has to re-authenticate by providing their username and password.

How long to set the JWT expiry time is tricky. If it's very long, it's more likely that a different person may use the same device to access the website, and the previous user's account will still be logged in. If it's very short though, it's really annoying for users.

This is where the concept of **token refreshing** comes into play.

We can provide our users two tokens: an **access token** that they can use to, well, access endpoints, and a **refresh token** that they can use to get a new access token without having to provide their username and password.

:::tip When do clients use the refresh token?
When a client makes a request and sends the access token, if the token has expired our API sends back a message to that effect.

At that point, the client can then, behind the scenes and without the user noticing, use the refresh to get a new access token, and re-request the original page.

For a client, the authentication flow is a three-step process:

1. Send the access token they've got stored (may or may not be fresh).
2. If API responds with a 401 Unauthorized, use the refresh token to get a new access token and try again. Now you've got a new, non-fresh access token.
3. If the API responds with another 401 Unauthorized, ask the user to log in again. Now you've got a fresh access token.
:::

The important thing here is **token freshness**. 

- A **fresh access token** is given to users immediately after logging in.
- A **non-fresh access token** is given to users when they use their refresh token.

This is important, because it means that we can protect certain routes by requiring a fresh access token. Since these tokens are only generated in response to login, we know that the user is probably who they say they are, and they haven't simply forgotten to log out.

As an example, if the user goes to their "delete my account" page, we might want a fresh token to access that endpoint. However, if they're simply going to their profile page, we may accept a non-fresh token.

## How to create refresh tokens with Flask-JWT-Extended

When a user logs in, we can create the access token and the refresh token at the same time. We will also make sure that the access token is marked as **fresh**.

First, let's add new imports:

```diff title="resources/user.py"
from flask_jwt_extended import (
    create_access_token,
+   create_refresh_token,
+   get_jwt_identity,
    get_jwt,
    jwt_required,
)
```

Then let's change our `UserLogin` route:

```python title="resources/user.py"
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            # highlight-start
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
            # highlight-end

        abort(401, message="Invalid credentials.")
```

## Writing the token refresh endpoint

When a user logs in, they will now have the access token and the refresh token.

Let's code another endpoint that will take the refresh token and return a new, non-fresh access token:

```python title="resources/user.py"
@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200
```

Note that above, we've told Flask-JWT-Extended that a refresh token is required with `@jwt_required(refresh=True)`. We'll do something similar for requiring fresh tokens in a second!

## Requiring a fresh token for certain endpoints

Let's go to the create item endpoint and mark it as needing a fresh token. Normally, fresh tokens would be required for destructive operations such as changing passwords or deleting accounts.

```python title="resources/item.py"
# highlight-start
@jwt_required(fresh=True)
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

## Error handling when a fresh token is required

When a fresh token is required but a non-fresh token is provided, we want the Flask app to return a message to that effect. We can do this just as we did with the other Flask-JWT-Extended configurations:

```python title="app.py"
@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "description": "The token is not fresh.",
                "error": "fresh_token_required",
            }
        ),
        401,
    )
```