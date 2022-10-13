# Populating and consuming the task queue with rq

We'll be using the [`rq` library](https://python-rq.org/) for our task queue implementation. Another popular option is `celery`, which is substantially more complex. For most workloads, `rq` is sufficient and it's much easier to work with.

First install the library:

```bash
pip install rq
```

And remember to add it to your `requirements.txt`

```text title="requirements.txt"
rq
```

Then it's helpful if we move the task code out to a separate file. Let's take our `send_simple_message` function and move it to `tasks.py`:

```py title="tasks.py"
import os
import requests
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")

def send_simple_message(to, subject, body):
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": f"Your Name <mailgun@{DOMAIN}>",
            "to": [to],
            "subject": subject,
            "text": body}
    )
```

Here I moved the domain line outside the function so it only runs once, and I've made sure to run `load_dotenv()` before it is requested.

The background worker will import `tasks.py` once at the start of its lifetime, so doing this will (very slightly) improve performance.

We could leave it like this, but I think we can do better. Let's write another function underneath that one that specifically describes the task that we want to perform in the background: send a registration email to a specific user:

```py title="tasks.py"
import os
import requests
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")

def send_simple_message(to, subject, body):
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": f"Your Name <mailgun@{DOMAIN}>",
            "to": [to],
            "subject": subject,
            "text": body}
    )


# highlight-start
def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        "Successfully signed up",
        f"Hi {username}! You have successfully signed up to the Stores REST API.",
    )
# highlight-end
```

:::tip
Remember to change "Your Name" in `from` to whatever name you want your emails to come from!
:::

Next up, add the Redis connection string that we got in the [previous section](../what_is_task_queue) to the `.env` file:

```text title=".env"
REDIS_URL="<insert your Redis url here>"
```

And then let's go to our User resource and add a couple of imports:

```py title="resources/user.py"
import redis
from rq import Queue
from tasks import send_user_registration_email
```

Then let's connect to Redis and create our `rq` queue. Under the blueprint definition, I'll add these lines:

```py title="resources/user.py"
connection = redis.from_url(
    os.getenv("REDIS_URL")
)  # Get this from Render.com or run in Docker
queue = Queue("emails", connection=connection)
```

Now we can use the `queue` to "enqueue" jobs, i.e. add to the queue. That will put some data into the Redis database, which then the background worker can consume.

### How to enqueue a job using `rq`

This is the easy part!

We are going to remove the code that sends the email from `resources/user.py`, and instead enqueue it using the `queue` variable. This takes the name of the function we want the background worker to call, and then all the arguments we'd like to pass to that function when it runs.

```diff title="resources/user.py"
-send_simple_message(
-    to=user.email,
-    subject="Successfully signed up",
-    body=f"Hi {user.username}! You have successfully signed up to the Stores REST API."
-)
+queue.enqueue(send_user_registration_email, user.email, user.username)
```

:::info
Remember the `send_user_registration_email` function doesn't run when we call `.enqueue`. It runs when the background worker starts working on this task, which could take some time!
:::