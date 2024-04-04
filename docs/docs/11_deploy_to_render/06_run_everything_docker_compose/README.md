# How to run the app and database with Docker Compose

Up until now we've been running `docker compose up` to start the REST API container.

Now let's modify our `docker-compose.yml` file to include spinning up a new PostgreSQL database.

```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:80"
    depends_on:
      - db
    env_file:
      - ./.env
    volumes:
      - .:/app
  db:
    image: postgres
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
```

The `postgres` image accepts various environment variables, among them:

- `POSTGRES_PASSWORD`, defaulting to `postgres`
- `POSTGERS_DB`, defaulting to `postgres`
- `POSTGRES_USER`, defaulting to `postgres`
- `POSTGRES_HOST`, defaulting to `localhost`
- `POSTGRES_PORT`, defaulting to `5432`

We should at least set a secure password. Above we're changing the password and database to `password` and `myapp` respectively.

:::caution
Remember to also change your `DATABASE_URL` in your `.env` file that the REST API container is using. It should look like this:

```
DATABASE_URL=postgresql://postgres:password@db/myapp
```

When Docker Compose runs, it creates a virtual network[^1] which allows you to connect to `db`, which connects to the running `db` service container.
:::

## Named volumes in Docker Compose

You'll notice that our `docker-compose.yml` file has these lines:

```
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
```

The bottom two lines define a named volume. This is data that will be stored by Docker and can be reused across container runs. We're calling it `postgres_data`, but it isn't assigned to anything there.

In the top two lines, which are part of the `db` service definition, we say that the `postgres_data` named volume is mapped to `/var/lib/postgresql/data` in the container.

`/var/lib/postgresql/data` is where the `postgres` image saves PostgreSQL data (such as databases, tables, etc). Therefore, as you create databases, tables, and store data, the named volume `postgres_data` will contain them.

When you restart the container (or even rebuilt it), you can use the same named volume to keep access to old data.

If you want to delete the entire database content, you can do so by deleting the volume through Docker Desktop, or with this command:

```
docker compose down -v
```

## Starting the whole system

Now you're ready to start the Docker Compose system! If you need to rebuild the REST API container first, run:

```
docker compose up --build --force-recreate --no-deps web
```

You'll get an error due to no database being available. That's OK, as long as the container is rebuilt!

Then press `CTRL+C` to stop it, and start the whole system with:

```
docker compose up
```

Now you can make a request to your API on port 5000, and it should work, storing the data in the database!

## Running the system in background mode

When we run the system with `docker compose up`, it takes up the terminal until we stop it with `CTRL+C`.

If you want to run it in "Daemon" mode, or in the background, so you can use the terminal for other things, you can use:

```
docker compose up -d
```

Then to stop the system, use:

```
docker compose down
```

Note you must be in the folder that contains your `docker-compose.yml` file in order to bring the system up or down.

:::warning
Running `docker compose down` will **not** delete your named volumes. You need to use the `-v` flag for that. Deleting the named volumes deletes the data in them irreversibly.
:::

[^1]: [Networking in Compose (official docs)](https://docs.docker.com/compose/networking/)