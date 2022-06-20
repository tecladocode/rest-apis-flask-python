---
title: Why use database migrations?
description: Learn about database migrations and what they are useful for.
---

# Why use database migrations?

As you work on your application, particularly over a long time, it is unavoidable that you will want to add columns to your models, or even add new models entirely.

Making the changes directly to the models without something like Alembic and Flask-Migrate will mean that the existing database tables and the model definitions will be out of sync. When that happens, SQLAlchemy usually complains and your application won't work.

An option is to delete everything and get SQLAlchemy to re-create the tables. Obviously, this is not good if you have data in the database as you would lose all the data.

We can use Alembic to detect the changes to the models, and what steps are necessary to "upgrade" the database so it matches the new models. Then we can use Alembic to actually modify the database following the upgrade steps.

Alembic also tracks each of these migrations over time, so that you can easily go to a past version of the database. This is useful if bugs are introduced or the feature requirements change.

Since Alembic tracks all the migrations over time, we can use it to create the tables from scratch, simply by applying the migrations one at a time until we reach the latest one (which should be equal to the current one).