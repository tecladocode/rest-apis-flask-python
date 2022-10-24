---
title: Getting set up
description: Set up a Flask project and create the Flask app.
---

# Getting set up

import VideoEmbed from "@site/src/components/VideoEmbed";

<div style={{ maxWidth: "720px", margin: "3rem auto", boxShadow: "0 5px 15px 0 rgba(0, 0, 0, 0.15)" }}>
<VideoEmbed url="https://customer-zmitazl0ztnd2pvm.cloudflarestream.com/42b7de55034431b4c4c9420460f8df7d/iframe?poster=https%3A%2F%2Fcustomer-zmitazl0ztnd2pvm.cloudflarestream.com%2F42b7de55034431b4c4c9420460f8df7d%2Fthumbnails%2Fthumbnail.jpg%3Ftime%3D%26height%3D600" />
</div>

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