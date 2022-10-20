# Sending emails when users register

If we want to be able to send emails to users when they register, we'll need to:

- Add an `email` column to the user model.
- Collect user email addresses when users register.

Let's begin with the model.

## Add an `email` column to the user model

```diff title="models/user.py"
+    email = db.Column(db.String, unique=True, nullable=False)
```

Then run the migration as we've already learned, to generate the migration script and upgrade the database to include the new column:

```bash
flask db migrate
```

Now let's check the migration script. It should include adding the `email` column, and making it unique.

Make sure that the `UniqueConstraint` is given a name. Alembic won't do this for you. Instead, it gives it the name `None` by default:

```py
op.create_unique_constraint(None, 'users', ['email'])
```

Change that to this:

```py
op.create_unique_constraint("email", 'users', ['email'])
```

And also when dropping the constraint:

```py
op.drop_constraint("email", 'users', type_='unique')
```

```bash
flask db upgrade  # make sure this is using the local dev database
```

## Collect user email addresses when they register

To do this, first let's add an `email` field to the incoming data. Remember that we use the `UserSchema` for this in our API, but at the moment we are using `UserSchema` for two things: registration and login.

If we modify `UserSchema` to add an email field, users will need to give us their username, email, and password when they log in.

So it's better to keep two schemas: one for registration, which asks for an email, and one for login, which only asks for the username.

```py
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


# highlight-start
class UserRegisterSchema(UserSchema):
    email = fields.Str(required=True)
# highlight-end
```

:::info
You could also get rid of usernames and only use emails. You can use email/password for login in that case!
:::

Now that we've got that, we can actually use the email field to create our `UserModel` objects:

```py title="resources/user.py"
from schemas import UserSchema, UserRegisterSchema

...

@blp.route("/register")
class UserRegister(MethodView):
    # highlight-start
    @blp.arguments(UserRegisterSchema)
    # highlight-end
    def post(self, user_data):
...

        user = UserModel(
            username=user_data["username"],
            # highlight-start
            email=user_data["email"],
            # highlight-end
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
```

Now we can use the `send_simple_message` function [we defined earlier](../01_send_emails_python_mailgun/README.md#sending-emails-with-mailgun) to actually send an email!

```py title="resources/user.py"
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

        # highlight-start
        send_simple_message(
            to=user.email,
            subject="Successfully signed up",
            body=f"Hi {user.username}! You have successfully signed up to the Stores REST API."
        )
        # highlight-end

        return {"message": "User created successfully."}, 201
```

## Error handling duplicate emails

In our `UserRegister` resource we are checking for duplicate usernames, but we should also check for duplicate emails. Otherwise, if a user tries to sign up with an email that already exists in the database, they'll get an ugly error.

```py title="resources/user.py"
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
        
        # ... Method continues here ...
```

So voilà, we're now sending an email when a user signs up!

But sending an email can take a non-trivial amount of time... Wouldn't it be nice if we could offload the task of sending emails to another process, so that it happens in the background without our API user having to wait?