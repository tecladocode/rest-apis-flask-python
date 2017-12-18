## Overview

Flask-JWT adds JWT functionality to Flask in an easy to use manner. It gives you a lot of functionality out of the box, but sometimes we want to modify some of the configuration. This document walks through how to:

* Change the authentication endpoint (by default, `/auth`);
* Change the token expiration time (by default, `5 minutes`);
* Change the authentication key name (by default, `username`).

In addition, it covers how to retrieve the **currently logged in user** from any of our Flask app endpoints.

This tutorial assumes that you’ve followed the lectures and have set up Flask-JWT already! If you haven't done so yet, check out Section 5 of the [Udemy course](https://www.udemy.com/rest-api-flask-and-python/?couponCode=GITHUB).

## Before We Start

First, let’s take a look at what we already have here.
In our app.py file, we should already set up the JWT using the below code:

```python
from flask_jwt import JWT
from security import authenticate, identity

jwt = JWT(app, authenticate, identity)  # /auth
```

And in our security.py file, we should have something like this:

```python
from werkzeug.security import safe_str_cmp
from models.user import UserModel

def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
```

## Configuration

### Authentication URL

If we want to change the url to the authentication endpoint, for instance, we want to use ```/login``` instead of ```/auth```, we can do something like this:

```python
app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authenticate, identity)
```

**Important**: We added the second line of code to emphasize that we must change the JWT configuration parameters first, **before creating the `JWT` instance**. Otherwise, our confuguration won't take effect. All of the following configurations follow the same principle.

If you want to change multiple configurations, make sure to put them all before creating the `JWT` instance.

### Token Expiration Time

```python
# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

jwt = JWT(app, authenticate, identity)
```

### Authentication Key Name

```python
# config JWT auth key name to be 'email' instead of default 'username'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

jwt = JWT(app, authenticate, identity)
```

### Other Configurations

You may find out more configuration options here: https://pythonhosted.org/Flask-JWT/

Please refer to the \<Configuration Options> section.

## More

### Retrieving User From Token

Another frequently asked question is: *how can I get the user's identity from an access token (JWT)?* Since in some cases, we not only want to guarantee that only our users can access this endpoint, we may want to access the user's data as well. For example, you want to restrict the access to a certain user group, not for every user. In this case, you can do something like this:

```python
from flask_jwt import jwt_required,current_identity


class User(Resource):

    @jwt_required()
    def get(self):   # view all users
        user = current_identity
        # then implement admin auth method
        ...
```

Now this endpoint is protected by JWT. And you have access to the identity of the user who is interacting with this endpoint using `current_identity` from JWT.
