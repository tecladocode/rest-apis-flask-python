---
title: Flask-JWT-Extended setup
description: Install and set up the Flask-JWT-Extended extension with our REST API.
---

# Flask-JWT-Extended setup

First, let's update our requirements:

```diff title="requirements.txt"
+ flask-jwt-extended
```

Then we must do two things:

- Add the extension to our `app.py`.
- Set a secret key that the extension will use to _sign_ the JWTs.

```python title="app.py"
from flask import Flask
from flask_smorest import Api
# highlight-start
from flask_jwt_extended import JWTManager
# highlight-end

from db import db

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    api = Api(app)

    # highlight-start
    app.config["JWT_SECRET_KEY"] = "jose"
    jwt = JWTManager(app)
    # highlight-end

    with app.app_context():
        import models  # noqa: F401

        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    return app
```

:::caution
The secret key set here, `"jose"`, is **not very safe**.

Instead you should generate a long and random secret key using something like `str(secrets.SystemRandom().getrandbits(128))`.
:::
