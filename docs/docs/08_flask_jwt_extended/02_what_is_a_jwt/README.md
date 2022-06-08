---
title: What is a JWT?
description: Understand what a JWT is, what data it contains, and how it may be used.
---

# What is a JWT?

A JWT is a signed JSON object with a specific structure. Our Flask app will sign the JWTs with the secret key, proving that _it generated them_.

The Flask app generates a JWT when a user logs in (with their username and password). In the JWT, we'll store the user ID. The client then stores the JWT and sends it to us on every request.

Because we can prove our app generated the JWT (through its signature), and we will receive the JWT with the user ID in every request, we can _treat requests that include a JWT as "logged in"_.

For example, if we want certain endpoints to only be accessible to logged-in users, all we do is require a JWT in them. Since the client can only get a JWT after logging in, we know that including a JWT is proof that the client logged in successfully at some point in the past.

And since the JWT includes the user ID inside it, when we receive a JWT we know _who logged in_ to get the JWT.

There's a lot more information about JWTs here: [https://jwt.io/introduction](https://jwt.io/introduction). This includes information such as:

- What is stored inside a JWT?
- Are JWTs secure?
