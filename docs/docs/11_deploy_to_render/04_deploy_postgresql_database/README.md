---
ctslug: how-to-get-a-deployed-postgresql-database
---

# How to get a deployed PostgreSQL database for our app

There are many PostgreSQL-as-a-Service providers (that means, services that handle creating and maintaining your database for you).

Render.com offers PostgreSQL, and the pricing is actually quite fair. However, the free tier is limited and you can only use it for a certain amount of time.

That's why I recommend using ElephantSQL for your free PostgreSQL needs. When you go over the free ElephantSQL limits, then you can use the Render.com database instead.

To get a free ElephantSQL PostgreSQL database, just go to their site, sign up, and then create a database in a region close to your Render.com server. Make sure to select the free tier.

![ElephantSQL screenshot showing plan configuration of Tiny Turtle (free) and name](https://res.cloudinary.com/teclado/image/upload/v1689180780/courses/rest-apis-flask-python/select-plan-and-name-elephantsql_sx3v2e.png)

Once you've got this, you should be able to see the Database URL:

![ElephantSQL screenshot showing that a copy icon beside the Database URL can be clicked to copy it](https://res.cloudinary.com/teclado/image/upload/v1689180780/courses/rest-apis-flask-python/copy-elephantsql-url_ydr90k.png)

Copy this, as you'll need it in the next lecture!
