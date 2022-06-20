---
title: Initialize your database with Flask-Migrate
description: "Learn the first steps when starting with Flask-Migrate: initializing the database."
---

# Initialize the database with Flask-Migrate

Activate your virtual environment and run this command:

```
flask db init
```

This will create a `migrations` folder inside your project folder.

In the `migrations` folder you'll find a few things:

- The `versions` folder is where migration scripts will be placed. These will be used by Alembic to make changes to the database.
- `alembic.ini` is the Alembic configuration file.
- `env.py` is a script used by Alembic to generate migration files.
- `script.py.mako` is the template file for migration files.

## Generate the first migration to set up the database

Now that we're set up, we need to make sure that the database we want to use is currently empty. In our case, since we're using SQLite, just delete `data.db`.

Then, run this command:

```
flask db migrate
```

This will create the migration file.


:::caution
It's important to double-check the migration script and make sure it is correct! Compare it with your model definitions and make sure nothing is missing.
:::

Now let's actually apply the migration:

```
flask db upgrade
```

This will create the `data.db` file. If you were using another RDBMS (like PostgreSQL or MySQL), this command would create the tables using the existing model definitions.

:::info How does the database know which version it's on?
When using Alembic to create the database tables from scratch, it creates an extra table with a single row, that stores the current migration version.

You'll note in each migration script there is information about the previous migration and the next migration.

This is why it's important to **never rename the migration files or change the revision identifiers at the top of those files**.
:::