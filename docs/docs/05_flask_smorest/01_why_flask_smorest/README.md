# Why use Flask-Smorest

There are many different REST API libraries for Flask. In a previous version of this course, we used Flask-RESTful. Now, I recommend using [Flask-Smorest](https://github.com/marshmallow-code/flask-smorest).

Over the last few months, I've been trialing the major REST libraries for Flask. I've built REST APIs using Flask-RESTful, Flask-RESTX, and Flask-Smorest.

I was looking to compare the three libraries in a few key areas:

- **Ease of use and getting started**. Many REST APIs are essentially microservices, so being able to whip one up quickly and without having to go through a steep learning curve is definitely interesting.
- **Maintainability and expandability**. Although many start as microservices, sometimes we have to maintain projects for a long time. And sometimes, they grow past what we originally envisioned.
- **Activity in the library itself**. Even if a library is suitable now, if it is not actively maintained and improved, it may not be suitable in the future. We'd like to teach something that you will use for years to come.
- **Documentation and usage of best practice**. The library should help you write better code by having strong documentation and guiding you into following best practice. If possible, it should use existing, actively maintained libraries as dependencies instead of implementing their own versions of them.
- **Developer experience in production projects**. The main point here was: how easy is it to produce API documentation with the library of choice. Hundreds of students have asked me how to integrate Swagger in their APIs, so it would be great if the library we teach gave it to you out of the box.

## Flask-Smorest is the most well-rounded

It ticks all the boxes above:

- If you want, it can be super similar to Flask-RESTful (which is a compliment, really easy to get started!).
- It uses [marshmallow](https://marshmallow.readthedocs.io/en/stable/) for serialization and deserialization, which is a huge plus. Marshmallow is a very actively-maintained library which is very intuitive and unlocks very easy argument validation. Unfortunately Flask-RESTX [doesn't use marshmallow](https://flask-restx.readthedocs.io/en/latest/marshalling.html), though there are [plans to do so](https://github.com/python-restx/flask-restx/issues/59).
- It provides Swagger (with Swagger UI) and other documentations out of the box. It uses the same marshmallow schemas you use for API validation and some simple decorators in your code to generate the documentation.
- The documentation is the weakest point (compared to Flask-RESTX), but with this course we can help you navigate it. The documentation of marshmallow is superb, so that will also help.

## If you took an old version of this course...

Let me tell you about some of the key differences between a project that uses Flask-RESTful and one that uses Flask-Smorest. After reading through these differences, it should be fairly straightforward for you to look at two projects, each using one library, and compare them.

1. Flask-Smorest uses `flask.views.MethodView` classes registered under a `flask_smorest.Blueprint` instead of `flask_restful.Resource` classes.
2. Flask-Smorest uses `flask_smorest.abort` to return error responses instead of manually returning the error JSON and error code.
3. Flask-Smorest projects define marshmallow schemas that represent incoming data (for deserialization and validation) and outgoing data (for serialization). It uses these schemas to automatically validate the data and turn Python objects into JSON.

Throughout this section I'll show you how to implement these 3 points in practice, so if you've already got a REST API that uses Flask-RESTful, you'll find it really easy to migrate.

Of course, you can keep using Flask-RESTful for your existing projects, and only use Flask-Smorest for new projects. That's also an option! Flask-RESTful isn't abandoned or deprecated, so it's still a totally viable option.