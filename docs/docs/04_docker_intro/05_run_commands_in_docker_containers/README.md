# How to run commands inside a Docker container

If you run your API using Docker Compose, with the `docker compose up` command, you may also want to be able to execute arbitrary shell commands in the container.

For example, later on in the course we will look at database migrations.

To execute a database migration, we need to run a specific command, `flask db mgirate`.

If we use Docker Compose, we'll need to run the command inside the running container, and not in a local terminal.

You can run any arbitrary command in a running container like so:

```bash
docker compose exec web flask db migrate
```

This command is split into 4 parts:

- `docker compose`: uses the Docker Compose part of the Docker executable
- `exec`: used to run a command in a specific Docker Compose service
- `web`: which Docker Compose service to run the command in
- `flask db migrate`: the command you want to run

That's all! Just remember while following the course, that if I run any commands in my local terminal and you are using Docker Compose, you should precede the commands with `docker compose exec web`.
