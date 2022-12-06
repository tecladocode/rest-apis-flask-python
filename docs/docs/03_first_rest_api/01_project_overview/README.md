---
title: Project Overview
description: A first look at the project we'll build in this section.
---

# Overview of your first REST API

import VideoEmbed from "@site/src/components/VideoEmbed";

<div style={{ maxWidth: "720px", margin: "3rem auto", boxShadow: "0 5px 15px 0 rgba(0, 0, 0, 0.15)" }}>
<VideoEmbed url="https://customer-zmitazl0ztnd2pvm.cloudflarestream.com/cda9c0473bdc485a36905144f13f4d3f/iframe?poster=https%3A%2F%2Fcustomer-zmitazl0ztnd2pvm.cloudflarestream.com%2Fcda9c0473bdc485a36905144f13f4d3f%2Fthumbnails%2Fthumbnail.jpg%3Ftime%3D%26height%3D600" />
</div>

In this section we'll make a simple REST API that allows us to:

- Create stores, each with a `name` and a list of stocked `items`.
- Create an item within a store, each with a `name` and a `price`.
- Retrieve a list of all stores and their items.
- Given its `name`, retrieve an individual store and all its items.
- Given a store `name`, retrieve only a list of item within it.

This is how the interaction will go!

:::tip Insomnia files
Remember to get the Insomnia files for this section or for all sections [here](/insomnia-files/)!
:::

## Create stores

Request:

```
POST /store {"name": "My Store"}
```

Response:

```
{"name": "My Store", "items": []}
```

## Create items

Request:

```
POST /store/My Store/item {"name": "Chair", "price": 175.50}
```

Response:

```
{"name": "Chair", "price": 175.50}
```

## Retrieve all stores and their items

Request:

```
GET /store
```

Response:

```
{
    "stores": [
        {
            "name": "My Store",
            "items": [
                {
                    "name": "Chair",
                    "price": 175.50
                }
            ]
        }
    ]
}
```

## Get a particular store

Request:

```
GET /store/My Store
```

Response:

```
{
    "name": "My Store",
    "items": [
        {
            "name": "Chair",
            "price": 175.50
        }
    ]
}
```

## Get only items in a store

Request:

```
GET /store/My Store/item
```

Response:

```
[
    {
        "name": "Chair",
        "price": 175.50
    }
]
```