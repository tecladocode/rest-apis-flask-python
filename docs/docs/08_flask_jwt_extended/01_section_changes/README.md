---
title: Changes in this section
description: Overview of the API endpoints we'll use for user registration and authentication.
---

# Changes in this section

:::tip Insomnia files
Remember to get the Insomnia files for this section or for all sections [here](/insomnia-files/)!
:::

In this section we will add the following endpoints:

| Method         | Endpoint          | Description                                           |
| -------------- | ----------------- | ----------------------------------------------------- |
| `POST`         | `/register`       | Create user accounts given an `email` and `password`. |
| `POST`         | `/login`          | Get a JWT given an `email` and `password`.            |
| 🔒 <br/> `POST` | `/logout`         | Revoke a JWT.                                         |
| 🔒 <br/> `POST` | `/refresh`        | Get a fresh JWT given a refresh JWT.                  |
| `GET`          | `/user/{user_id}` | (dev-only) Get info about a user given their ID.      |
| `DELETE`       | `/user/{user_id}` | (dev-only) Delete a user given their ID.              |

We will also protect some existing endpoints by requiring a JWT from clients. You can see which endpoints will be protected in [The API we'll build in this course](/docs/course_intro/what_is_rest_api/#the-api-well-build-in-this-course)