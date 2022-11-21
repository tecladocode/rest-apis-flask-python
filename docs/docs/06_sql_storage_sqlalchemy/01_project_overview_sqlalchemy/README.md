---
title: Project Overview, and why use SQLAlchemy
description: Let's look at what we'll do in this section. There are no changes to the client-facing API at all, just changes internally to how we store data.
---

# Project Overview (and why use SQLAlchemy)

:::tip Insomnia files
Remember to get the Insomnia files for this section or for all sections [here](/insomnia-files/)!
:::

In this section we'll make absolutely no changes to the API! However, we will completely change the way we store data.

Up until now, we've been storing data in an "in-memory database": a couple of Python dictionaries. When we stop the app, the data is destroyed. This is obviously not great, so we want to move to a proper store that can keep data around between app restarts!

We'll be using a relational database for data storage, and there are many different options: SQLite, MySQL, PostgreSQL, and others.

At this point we have two options regarding how to interact with the database:

1. We can write SQL code and execute it ourselves. For example, when we want to add an item to the database we'd write something like `INSERT INTO items (name, price, store_id) VALUES ("Chair", 17.99, 1)`.
2. We can use an ORM, which can take Python objects and turn them into database rows.

For this project, we are going to use an ORM because it makes the code much cleaner and simpler. Also, the ORM library (SQLAlchemy) helps us with many potential issues with using SQL, such as:

- Multi-threading support
- Handling creating the tables and defining the rows
- Database migrations (with help of another library, Alembic)
- Like mentioned, it makes the code cleaner, simpler, and shorter

To get started, add the following to the `requirements.txt` file:

```text title="requirements.txt"
sqlalchemy
flask-sqlalchemy
```

<details>
  <summary>What is Flask-SQLAlchemy?</summary>
  <div>
    <p>SQLAlchemy is the ORM library, that helps map Python classes to database tables and columns, and turns Python objects of those classes into specific rows.</p>
    <p>Flask-SQLAlchemy is a Flask extension which helps connect SQLAlchemy to Flask apps.</p>
  </div>
</details>

With this, install your requirements (remember to activate your virtual environment first!).

```
pip install -r requirements.txt
```

Let's begin creating our SQLAlchemy models in the next lecture.