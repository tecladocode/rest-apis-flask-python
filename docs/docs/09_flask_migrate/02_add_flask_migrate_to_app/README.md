---
title: How to add Flask-Migrate to our Flask app
description: Integrating your Flask app with Flask-Migrate is relatively straightforward. Learn how to do it in this lecture.
---

# How to add Flask-Migrate to our Flask app

Adding Flask-Migrate to our app is simple, just install it and add a couple lines to `app.py`.

To install:

```bash
pip install flask-migrate
```

This will also install Alembic, since it is a dependency.

Then we need to add 2 lines to `app.py` (highlighted):

```py
from flask_smorest import Api
# highlight-start
from flask_migrate import Migrate
# highlight-end

import models

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
db.init_app(app)
# highlight-start
migrate = Migrate(app, db)
# highlight-end
api = Api(app)

with app.app_context():
    db.create_all()
```

Since we will be using Flask-Migrate to create our database, we no longer need to tell Flask-SQLAlchemy to do it when we create the app.

Delete these two lines:

```py
with app.app_context():
    db.create_all()
```
