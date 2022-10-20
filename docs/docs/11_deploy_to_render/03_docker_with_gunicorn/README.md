# Run our Flask app with gunicorn in Docker

Throughout the course, we've been working with a Docker image like this one:

```dockerfile
FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]
```

This is all well and good for local development, but when we deploy our application we want to run it with the best performance possible.

This is why we don't want to run the Flask development server and the Flask debugger. Instead, we'll use gunicorn to run our app.

## Run our Flask app with gunicorn

First let's add `gunicorn` to our `requirements.txt` file:

```text title="requirements.txt"
flask
flask-smorest
python-dotenv
sqlalchemy
flask-sqlalchemy
flask-jwt-extended
passlib
flask-migrate
# highlight-start
gunicorn
# highlight-end
```

Then, let's change our `Dockerfile` to use `gunicorn`:

```dockerfile
FROM python:3.10
WORKDIR /app
COPY ./requirements.txt requirements.txt
# highlight-start
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# highlight-end
COPY . .
# highlight-start
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]
# highlight-end
```

The `CMD` line change is the important one, as it runs `gunicorn` on port `80`, and we pass in the app factory function.

:::tip
Note I've also changed the `pip install` line. Adding `--no-cache-dir` and `--upgrade` just makes sure we can't accidentally install from a cache directory (which shouldn't exist anyway!), and that we'll upgrade to the latest possible versions allowed by our `requirements.txt` file.
:::

## Run the Docker container locally with the Flask development server and debugger

If you use this `Dockerfile`, it doesn't mean you can't run it locally using the Flask development server. You don't have to lose the automatic restarting capabilities, or the Flask debugger.

To run the Docker container locally, you'll have to do this from now on:

```zsh
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" teclado-site-flask sh -c "flask run --host 0.0.0.0"
```

This is similar to how we've ran the Docker container with our local code as a volume (that's what `-w /app -v "$(pwd):/app"` does), but at the end of the command we're telling the container to run `flask run --host 0.0.0.0` instead of the `CMD` line of the `Dockerfile`. That's what `sh -c "flask run --host 0.0.0.0"` does!

Now you're ready to commit and push this to your repository and re-deploy to Render.com!
