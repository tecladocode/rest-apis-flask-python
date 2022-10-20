---
title: Configure Flask-SQLAlchemy
description: Link Flask-SQLAlchemy with our Flask app and create the initial tables.
---

# Configure Flask-SQLAlchemy

We want to add two imports to `app.py`:

```python title="app.py"
from db import db

import models
```

## The Flask app factory pattern

Up until now, we've been creating the `app` variable (which is the Flask app) directly in `app.py`.

With the app factory pattern, we write a function that _returns_ `app`. That way we can _pass configuration values_ to the function, so that we configure the app before getting it back.

This is especially useful for testing, but also if you want to do things like have staging and production apps.

To do the app factory, all we do is place all the app-creation code inside a function which **must be called `create_app()`**.

```python title="app.py"
from flask import Flask
from flask_smorest import Api

from db import db

import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

# highlight-start
def create_app():
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    api = Api(app)

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app
# highlight-end
```

## Add Flask-SQLAlchemy code to the app factory

```python title="app.py"
from flask import Flask
from flask_smorest import Api

from db import db

import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

# highlight-start
def create_app(db_url=None):
    # highlight-end
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # highlight-start
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    # highlight-end
    api = Api(app)

    # highlight-start
    with app.app_context():
        db.create_all()
    # highlight-end

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app
```

We've done three things:

1. Added the `db_url` parameter. This lets us create an app with a certain database URL, or alternatively try to fetch the database URL from the environment variables. The default value will be a local SQLite file, if we don't pass a value ourselves and it isn't in the environment.
2. Added two SQLAlchemy values to `app.config`. One is the database URL (or URI), the other is a [configuration option](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/) which improves performance.
3. When the app is created, tell SQLAlchemy to create all the database tables we need.

:::tip How does SQLAlchemy know what tables to create?
The line `import models` lets SQLAlchemy know what models exist in our application. Because they are `db.Model` instances, SQLAlchemy will look at their `__tablename__` and defined `db.Column` attributes to create the tables.
:::