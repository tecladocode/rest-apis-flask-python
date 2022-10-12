# Define e-mail sending tasks with RQ

In `.env`:

```text
MAILGUN_DOMAIN=sandbox8vb7a9v7ba76vva.mailgun.org
```

In `tasks.py`:

```py
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


def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        "Successfully signed up",
        f"Hi {username}! You have successfully signed up to the Stores REST API.",
    )
```

Then in the user resource, change to this:

```py
from redis import Redis
from rq import Queue
from schemas import UserSchema, UserRegisterSchema
from tasks import send_user_registration_email

connection = Redis("REDIS_URL")  # Get this from Render.com or run in Docker
queue = Queue("emails", connection=connection)

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        queue.enqueue(send_user_registration_email, user)

        return {"message": "User created successfully."}, 201
```
