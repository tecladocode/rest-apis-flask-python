# How to use Environment Variables in Render.com

A common way to configure applications before they start up is by using environment variables.

We can define environment variables in our computers, and also in our servers, and of course they can be different in each.

That's what's interesting about them: we can define an environment variable locally for our database, which may be `sqlite:///data.db`. Then in our server we can define the same variable, but with a value of the ElephantSQL Database URL.

Since we are using SQLAlchemy in our application, it doesn't care whether it's connecting to SQLite or PostgreSQL. So all we have to do to use a different database is change the connection string.

Let's begin by using environment variables locally.

## How to use environment variables locally with our Flask app

First, let's create a new file called `.env`. In this file, we can store any environment variables we want. We can then "load" these variables when we start the app.

```text title=".env"
DATABASE_URL=sqlite:///data.db
```

With the file created, we can load it when we start our Flask app:

```python title="app.py"
# highlight-start
import os
# highlight-end
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
# highlight-start
from dotenv import load_dotenv
# highlight-end

from db import db
from blocklist import BLOCKLIST

from resources.user import blp as UserBlueprint
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    # highlight-start
    load_dotenv()
    # highlight-end
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
    # highlight-end
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    api = Api(app)
```

Highlighted are four lines which we must change.

1. First we `import os`. We'll need this to access environment variables.
2. Second, we import the `load_dotenv` function, which we'll need to run in order to turn the contents of the `.env` file into environment variables.
3. We actually run the `load_dotenv` function.
4. We'll use `db_url` if provided, otherwise we'll retrieve the environment variable's value. If there is no environment value, the default will be `"sqlite:///data.db"`.

Notice that our Flask app has two ways to be configured: with the `db_url` argument, or via environment variables. You would normally use `db_url` when writing automated tests for your application. While we don't do that in this course, it's a good habit to get into!

:::warning
Do not include your `.env` file in your GitHub repository! Add it to `.gitignore` so you don't include it accidentally.
:::

Since we can't include `.env` in our GitHub repository, we should do something to make sure that new developers know that they should create a `.env` file when they clone the repository.

We normally do this by creating a file called `.env.example`. This file should only contain the environment variable definitions, but not the values:

```text title=".env.example"
DATABASE_URL=
```

You should add `.env.example` to your repository.

Commit the changes, and push them to GitHub. We'll need these changes so we can use environment variables in Render.com.

## How to add environment variables to Render.com

Now that our Flask app is using environment variables, all we have to do is add the `DATABASE_URL` environment variable to our Render.com service, and then deploy the latest changes from our GitHub repository.

To add environment variables in Render.com, go to the service settings and then on the left you'll see "Environment":

![Render.com screenshot showing the button to add a environment variables](./assets/render-add-env-var.png)

Click on "Add Environment Variable", and there put `DATABASE_URL` as the key, and your ElephantSQL Database URL as the value:

![Render.com screenshot showing DATABASE_URL added with a pixelated value](./assets/render-database-url-env-var.png)

Now, do another manual deploy of the latest commit (which should include your `app.py` changes to use environment variables).

When this is done, your app should be saving to the ElephantSQL database!
