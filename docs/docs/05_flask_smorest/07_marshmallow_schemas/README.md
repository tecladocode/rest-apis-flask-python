---
title: Adding marshmallow schemas
description: A marshmallow schema is useful for validation and serialization. Learn how to write them in this lecture.
---

# Adding marshmallow schemas

Something that we're lacking in our API at the moment is validation. We've done a _tiny_ bit of it with this kind of code:

```py
if (
    "price" not in item_data
    or "store_id" not in item_data
    or "name" not in item_data
):
    abort(
        400,
        message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
    )
```

But there's so much more we can do. For starters, some data points may be optional in some endpoints. We also want to check the data type is correct (i.e. `price` shouldn't be a string, for example).

To do this kind of checking we can construct a massive `if` statement, or we can use a library that is made specifically for it.

The `marshmallow`[^1] library is used to define _what_ data fields we want, and then we can pass incoming data through the validator. We can also go the other way round, and give it a Python object which `marshmallow` then turns into a dictionary.

## Writing the `ItemSchema`

Here's the definition of an `Item` using `marshmallow` (this is called a **schema**):

```py title="schemas.py"
from marshmallow import Schema, fields


class ItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)
```

A couple of weird things maybe!

The `id` field is a string, but it has the `dump_only=True` argument. This means that when we use marshmallow to _validate incoming data_, the `id` field won't be used or expected. However, when we use marshmallow to _serialize_ data to be returned to a client, the `id` field will be included in the output.

The other fields will be used for both validation and serialization, and since they have the `required=True` argument, that means that when we do validation if the fields are not present, an error will be raised.

`marshmallow` will also check the data type with `fields.Float` and `fields.Int`.

## Writing the `ItemUpdateSchema`

Something that even to do this day sits a bit weird with me is having multiple different schemas for different applications.

When we want to update an Item, we have different requirements than when we want to create an item.

The main difference is that the incoming data to our API when we update an item is different than when we create one. Fields are optional, such that not all item fields should be required. Also, you may not want to allow certain fields _at all_.

This is the `ItemUpdateSchema`:

```py title="schemas.py"
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
```

As you can see, these are not `required=True`. I've also taken off the `id` and `store_id` fields, because:

- This schema will only be used for incoming data, and we will never receive an `id`.
- We don't want clients to be able to change the `store_id` of an item. If you wanted to allow this, you can add the `store_id` field here as well.

## Writing the `StoreSchema`

```py title="schemas.py"
class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
```

There's not much to explain here! Similar to the `ItemSchema`, we have `id` and `name` since those are the only fields we need for a store.