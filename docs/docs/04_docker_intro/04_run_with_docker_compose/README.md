# Run the REST API using Docker Compose

Now that we've got a Docker container for our REST API, we can set up Docker Compose to run the container.

Docker Compose is most useful to start multiple Docker containers at the same time, specifying configuration values for them and dependencies between them.

Later on, I'll show you how to use Docker Compose to start both a PostgreSQL database and the REST API. For now, we'll use it only for the REST API, to simplify starting its container up.

If you have Docker Desktop installed, you already have Docker Compose. If you want to install Docker Compose in a system without Docker Desktop, please refer to the [official installation instructions](https://docs.docker.com/compose/install/).

## How to write a `docker-compose.yml` file

Create a file called `docker-compose.yml` in the root of your project (alongside your `Dockerfile`). Inside it, add the following contents:

```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
```

This small file is all you need to tell Docker Compose that you have a service, called `web`, which is built using the current directory (by default, that looks for a file called `Dockerfile`).

Other settings provided are:

- `ports`, used to map a port in your local computer to one in the container. Since our container runs the Flask app on port 5000, we're targeting that port so that any traffic we access in port 5000 of our computer is sent to the container's port 5000.
- `volumes`, to map a local directory into a directory within the container. This makes it so you don't have to rebuild the image each time you make a code change.

## How to run the Docker Compose services

Simply type:

```
docker compose up
```

And that will start all your services. For now, there's just one service, but later on when we add a database, this command will start everything.

When the services are running, you'll start seeing logs appear. These are the same logs as for running the `Dockerfile` on its own, but preceded by the service name.

In our case, we'll see `web-1  |  ...` and the logs saying the service is running on `http://127.0.0.1:5000`. When you access that URL, you'll see the request logs printed in the console.

Congratulations, you've ran your first Docker Compose service!

## Rebuilding the Docker image

If you need to rebuild the Docker image of your REST API service for whatever reason (e.g. configuration changes), you can run:

```
docker compose up --build --force-recreate --no-deps web
```

More information [here](https://stackoverflow.com/a/50802581).
