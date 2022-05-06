---
title: "What is a REST API?"
description: "There's a lot of confusion around what is and isn't a REST API. Let's take a look!"
---

# What is a REST API?

## What is an API?

API stands for "Application Programming Interface", but that's not an overly helpful name!

The most important part of the term is "Interface". Just as the interface to a car is the parts we humans interact with (steering wheel, pedals, gear stick), the interface to an application is the code that another application can interact with.

This way, any part of an application that can be "called" or "executed" from another application, is part of that application's API.

For example, let's say you make a simple Python library to save data to a database. This is what the library looks like:

```py
def save_to_db(what_to_save):
    pass


def get_from_db(query):
    pass
```

Assume that the functions are implemented and they do something!

This "library" has an API: the `save_to_db` and `get_from_db` functions. These are the functions that the library makes available to other programs (or parts of programs), which those other programs should use to save and get data from a database.

If you look at it this way, almost everything in programming has at least an "interface".

As another example, when you code a class, it has an interface: the public attributes and methods.

So the key to an API is that it has to be publicly callable, and it allows the _client_ (whoever calls it) to interact with the program that offers the API.

### An API with Flask

When we make Flask apps, we also have some public functions that can be called. Our public functions are each associated to an endpoint, such as `/store`.

That way a client (such as another Python program, or even a web browser) can access the `/store` endpoint of our application, and we can run some code and return a value.

If our Flask app is hosted at `http://my-flask-app.com`, then accessing `http://my-flask-app.com/store` would execute the function associated with the `/store` endpoint in our app, and the client would receive the data returned by the associated function.

That data might look like this:

```json
{
    "stores": [
        {
            "name": "My Store",
            "items": [
                {
                    "name": "my item",
                    "price": 15.99
                }
            ]
        }
    ]
}
```

### The purpose of APIs

Okay, we've learned that we can make a Flask app and expose certain functions to the public by using endpoints. Clients can then make requests (we'll learn how later), and get data.

Clients can also send data, which the functions can use.

But _why_? If you want to use certain functions, why not just code them in your application?

There's one main reason: so two or more clients can use the API without having to duplicate the logic that the API offers inside their own code.

Let's say you want to build a weather app.

You could try to install sensors at the top of your house, connect them directly to the computer running your code, and then offer weather info based on what the sensors say...

Or you could request weather data from the OpenWeatherMap API, just as tens of thousands of other devices do. 

Much easier, and all you have to do is make a request to the API!

### Making an API for your own consumption

Make software companies make APIs that only they use (so they aren't fully public).

Here's an example. You're making a multiplayer mobile game, and you need to store information about the moves that your character is making.

In your mobile app code, you could connect to a central database and store the moves there. Apps in other mobile devices would also connect to the central database and store (and read) the moves from there.

But what happens when you want to expand your app to other devices? Let's say, iOS and Android?

Then you've got to duplicate your database logic in two places: the two app codebases. The problem is compounded if you want to expand to computers, consoles, etc.

It's easier to have an API which exposes certain functions that let your app save and retrieve data from a database, and have all your devices use that same API.

It will be much simpler, and when you want to make database changes you most likely won't have to change the code of each mobile app.

## What is REST?

Now that you know what an API is, a slightly more difficult question to answer is "What is a REST API?".

A REST API is just an API that follows specific conventions and has specific characteristics.

REST APIs deal in resources, so every individual "thing" that can be named is a resource. For example, stores, items, tags, users, or less concrete things like temporal services or collections of other resources.

The main characteristics (or constraints) of a REST API are:

1. **Uniform interface**. Whichever way clients should access a certain resource should also be the way the access other resources. Clients should have a single way to retrieve resources.
2. **Client-server**. Clients should know the endpoints of the API, but they should not be coupled to the development of the API. A client or a servevr may be swapped out for a different implementation without the other noticing.
3. **Stateless**. The server (API) doesn't store anything about previous client requests. Each client request is treated as a brand new client. If the client needs the server to personalize the response, then the client must send the server whatever information the server needs in order to do so.
4. **Cacheable**. The client or server must be able to cache the resources returned by the API. This is a very general constraint, but it's an important one.
5. **Layered system**. REST APIs may be developed as multiple layers, where each layer interacts [only with the layer above and below it](https://excalidraw.com/#json=or3Umoigss4yIeuKg3cO8,qH6uDDCXc7DSjweqNvlmzw).

If you'd like to read a very complete and exhaustive guide about everything that a REST API is, check out [this guide](https://restfulapi.net/).