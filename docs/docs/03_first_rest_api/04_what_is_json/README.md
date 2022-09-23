---
title: "What is JSON?"
description: JSON is the way we normally transfer data to and from REST APIs.
---

# What is JSON?

JSON is just a (usually long) string whose contents follow a specific format.

One example of JSON:

```json
{
    "key": "value",
    "another": 25,
    "listic_data": [
        1,
        3,
        7
    ],
    "sub_objects": {
        "name": "Rolf",
        "age": 25
    }
}
```

So at its core, you've got:

- Strings
- Numbers
- Booleans (`true` or `false`)
- Lists
- Objects (akin to dictionaries in Python)
  - Note that objects are not ordered, so the keys could come back in any order. This is not a problem!

At the top level of a piece of JSON you can have an object or a list. So this is also valid JSON:

```json
[
    {
        "name": "Rolf",
        "age": 25
    },
    {
        "name": "Anne",
        "age": 27
    },
    {
        "name": "Adam",
        "age": 23
    }
]
```

When we return a Python dictionary in a Flask route, Flask automatically turns it into JSON for us, so we don't have to.

Remember that "turning it into JSON" means two things:

1. Change Python keywords and values so they match the JSON standard (e.g. `True` to `true`).
2. Turn the whole thing into a single string that our API can return.

:::tip
Note that JSON can be "prettified" (as the above examples), although usually it is returned by our API "not-prettified":

```json
[{"name":"Rolf","age":25},{"name":"Anne","age":27},{"name":"Adam","age":23}]
```

This removal of newlines and spaces, believe it or not, adds up and can save a lot of bandwidth since there is less data to transfer between the API server and the client.
:::