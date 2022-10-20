# What is a task queue?

A queue is a data structure to which you can add and remove data, but a key aspect of it is that when you want to remove a piece of data from it, the piece of data removed is the first piece of data that was added.

![New elements are added at the end, called pushing, and removed from the start, called popping, of a queue](./assets/queues.drawio.png)

This is identical to how people queuing works. The first person to arrive at the queue (i.e. the first in line), is the first person removed from the queue when they reach the ticket counter.

We need a queueing system for our email sending so that when we offload tasks, we put them in a queue. Then we will have a separate program (the **background worker**), taking items from the queue one at a time and processing them.

Each item in the queue will be an email to be sent (or rather, information so that the background worker can send the email).

## Setting up the Redis database for our queue

We can use the Redis database to store our queue of tasks. There are alternative options, such as RabbitMQ, but we won't cover them in this course.

You can install Redis in a few different ways:

- Install it locally by following their guides.
- Install it using Docker (I recommend this for a local install).
- Use a Redis database in the cloud so you don't have to install anything (this is what we do in the video).

Render.com can provide us with a free Redis database, so I recommend using that to get started.

Navigate to your Render.com dashboard, and create a new free Redis database. The free Redis provided doesn't have persistence enabled, but that's okay. It means we will lose data if the service is turned off, but since we're using it as a task queue that's not as big a deal as it otherwise could be.

Later on if we want, we can upgrade to one of the paid plans.

To be able to add tasks to the queue from your dev environment, make sure to [allow external connections](https://render.com/docs/redis#connecting-to-your-redis-from-outside-render) in your Redis database configuration.

![Screenshot showing 0.0.0.0/0 as an allowed IP address when connecting to our Render Redis database](./assets/render-redis-allowing-outside.png)

You should get a Redis URL that looks like this: `rediss://red-ct8aen0hkl10:MnLs0mmrX7MBXWRkdrh49@frankfurt-redis.render.com:6379`. Save it, for we'll need it in the next lecture!
