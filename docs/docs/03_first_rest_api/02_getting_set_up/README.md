---
title: Getting set up
description: Set up a Flask project and create the Flask app.
---

# Getting set up

Create a virtual environment and activate it.
   
```
python3.10 -m venv .venv
source .venv/bin/activate
```

Install Flask.
   
```
pip install flask
```

Create a file for the Flask app (I like to call it `app.py`)
Create the Flask app.

```py title="app.py"
from flask import Flask

app = Flask(__name__)
```

Now you can run this app using the Flask Command-Line Interface (CLI):

```
flask run
```

But the app doesn't do anything yet! Let's work on our first API endpoint next.