# What is a Docker container?

I'm sure you have heard of the term "Virtual Machine". A Virtual Machine is an emulation of an Operating System.

This means that you can run a Windows Virtual Machine on a computer running Mac OS. When you do that, you can have the Windows Operating System running inside an app in your Mac.

When you run a Virtual Machine, you can configure what hardware it has access to (e.g. 50% of the host's RAM, 2 CPU cores, etc).

Docker containers are a bit different because they don't emulate an Operating System. They use the Operating System kernel of your computer, and run as a process within the host.

Containers have their own storage and networking, but because they don't have to emulate the operating system and everything that entails, they are much more lightweight and efficient. Another benefit of containers is that their start-up time is very fast.

There are pros and cons to both. For example, you can't run a Windows Docker container if you are using Mac OS in your machine. You'd have to run a Windows Virtual Machine, and then run Docker containers in that, which isn't very efficient!

:::caution
Because Docker containers use your OS kernel, you can run Linux images in a Mac OS container.

However, new Mac computers use a different CPU architecture (ARM), and this can pose problems in some cases. More on this later on!
:::

## What does a Docker container run?

If you want to run your Flask app in a Docker container, you need to get (or create) a Docker image that has all the dependencies your Flask app uses:

- Python
- Dependencies from `requirements.txt`
- Possibly nginx or gunicorn (more on this when we talk about deployment)

Let's take a look at Docker images in the next lecture.