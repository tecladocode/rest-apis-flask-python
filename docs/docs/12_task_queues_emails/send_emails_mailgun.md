# How to send e-mails using Postmark and Python

- Register for Mailgun (free trial, up to 5 recipients)
- Under "Sending", select the sandbox domain
- Enter a new "authorized recipient" and then confirm it by clicking the button on the e-mail you've received.
- Copy the "Python" code snippet which looks like this:

```py
def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages",
        auth=("api", "YOUR_API_KEY"),
        data={"from": "Excited User <mailgun@YOUR_DOMAIN_NAME>",
            "to": ["bar@example.com", "YOU@YOUR_DOMAIN_NAME"],
            "subject": "Hello",
            "text": "Testing some Mailgun awesomness!"})
```

- We will need this in a few moments!

```py
DOMAIN = "sandbox723b0599ff8148a08a38f9df9cfaf5d9.mailgun.org"
def send_simple_message(to, subject, body):
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY"),
        data={"from": f"Your Name <mailgun@{DOMAIN}>",
            "to": [to],
            "subject": subject,
            "text": body})
```

Make sure to have this in your `.env` file:

```env
POSTMARK_SERVER_API_TOKEN="751756815-5617a-158b98-bgb8a879858"
```

- Next we will send an e-mail to the user when they register.
- First let's add an e-mail column to our user model

```diff
+    email = db.Column(db.String, unique=True, nullable=False)
```

- Then run the migration as we've already learned.

```bash
flask db migrate
flask db upgrade  # make sure this is using the local dev database
```

Make the e-mail required through the schemas by creating a `UserRegisterSchema`:

```py
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class UserRegisterSchema(UserSchema):
    email = fields.Str(required=True)
```

And then in the User resource:

```py
from schemas import UserSchema, UserRegisterSchema

...

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
...

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
```

Now when a user registers, we can send an e-mail:

```py
import os
import requests

...

DOMAIN = "sandbox723b0599ff8148a08a38f9df9cfaf5d9.mailgun.org"
def send_simple_message(to, subject, body):
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": f"Your Name <mailgun@{DOMAIN}>",
            "to": [to],
            "subject": subject,
            "text": body}
    )

...

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

        send_simple_message(
            to=user.email,
            subject="Successfully signed up",
            body=f"Hi {user.username}! You have successfully signed up to the Stores REST API."
        )

        return {"message": "User created successfully."}, 201
```

We will also want to add some error handling on the unique e-mail column:

```py
from sqlalchemy import or_

...

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            or_(
                UserModel.username == user_data["username"],
                UserModel.email == user_data["email"]
            )
        ).first():
            abort(409, message="A user with that username or email already exists.")
```