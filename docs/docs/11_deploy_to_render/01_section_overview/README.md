# Overview of this section

:::tip Insomnia files
Remember to get the Insomnia files for this section or for all sections [here](/insomnia-files/)!
:::

In this section, we will figure out how to get our Flask app and put it on a public server so other people can interact with it! This is called "deploying".

There are many services we can use to deploy our app. Most of them have some sort of "free tier" so that you can try the deployment without having to pay anything. Usually, if you want better performance or unlimited usage, you have to pay.

Remember that just as we run the Flask app in our computers, when we deploy it the app runs in a server, somewhere in the world. For all intents and purposes, the server is just like our computer!

Servers usually run Linux, so we can deploy our Docker images without a performance hit as we would using Mac or Windows.

At the end of the section, you'll be able to access your API using a URL such as [https://rest-api-smorest-docker.onrender.com](https://rest-api-smorest-docker.onrender.com).

For this section, our deployment will be completely free. We will deploy our Flask app for free, and we will also get a free PostgreSQL database on the cloud using ElephantSQL.
