## Overview
This tutorial will cover some basic Flask-JWT configurations and help you customize it within your project. However, this tutorial will assume that you’ve followed the lectures and has set up Flask-JWT already.

## Before We Start
First, let’s take a look at what we already have here.
In our app.py file, we should already set up the JWT using the below code: 
```
from flask_jwt import JWT
from security import authenticate, identity
jwt = JWT(app, authenticate, identity)  # /auth
```
And in our security.py file, we should have something like this:

```
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
```
app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authenticate, identity)
```
We added the second line of code to emphasize that we must config JWT first 
before requesting a JWT instance, otherwise our confuguration won't take effect. The following configurations follow the same principle but we will omit the second line.
### Token Expiration Time
```
# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
```
### Authentication Key Name
```
# config JWT auth key name to be 'email' instead of default 'username'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
```
### Other Configurations
You may find out more configuration options here: https://pythonhosted.org/Flask-JWT/

Please refer to the \<Configuration Options> section.

## More
### Retrieving User From Token
Another frequently asked question is that how can I get the user's identity from an access token (JWT)? Since in some cases, we not only want to guarantee that only our users can access this endpoint, we want to make sure who he is as well. For example, you want to restrict the access to a certain user group, not for every user. In this case, you can do something like this:
```
from flask_jwt import jwt_required,current_identity


class User(Resource):

    @jwt_required()
    def get(self):   # view all users
        user = current_identity
        # then implement admin auth method
        ...
```
Now this endpoint is protected by JWT. And you have access to the identity of whom is interacting with this endpoint using ```current_identity``` from JWT.
