---
title: Your First REST API Endpoint
description: Learn how to define a REST API endpoint using Flask.
---

# Your First REST API Endpoint

import LockedVideoEmbed from "@site/src/components/LockedVideoEmbed";

<LockedVideoEmbed />

Let's start off by defining where we'll store our data. In most REST APIs, you'd store your data in a database. For now, and for simplicity, we'll store it in a Python list.

Later on we'll work on making this data dynamic. For now let's use some sample data.

```py title="app.py"
from flask import Flask

app = Flask(__name__)

stores = [{"name": "My Store", "items": [{"name": "my item", "price": 15.99}]}]
```

Now that we've got the data stored, we can go ahead and make a Flask route that, when accessed, will return all our data.

```py title="app.py"
from flask import Flask

app = Flask(__name__)

stores = [{"name": "My Store", "items": [{"name": "my item", "price": 15.99}]}]


@app.get("/store")
def get_stores():
    return {"stores": stores}
```

## Anatomy of a Flask route

There are two parts to a Flask route:

- The endpoint decorator
- The function that should run

The endpoint decorator (`@app.get("/store")`) _registers_ the route's endpoint with Flask. That's the `/store` bit. That way, the Flask app knows that when it receives a request for `/store`, it should run the function.

The function's job is to do everything that it should, and at the end return _something_. In most REST APIs, we return JSON, but you can return anything that can be represented as text (e.g. XML, HTML, YAML, plain text, or almost anything else).