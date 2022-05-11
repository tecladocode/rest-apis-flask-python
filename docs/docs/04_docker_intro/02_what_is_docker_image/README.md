# What is a Docker image?

A Docker image is a snapshot of source code, libraries, dependencies, tools, and everything else (except the Operating System kernel!) that a container needs to run.

There are many pre-built images that you can use. For example, some come with Ubuntu (a Linux distribution). Others come with Ubuntu and Python already installed. You can also make your own images that already have Flask installed (as well as other dependencies your app needs).

Creating a Docker image is straightforward (when you know how!). I'll guide you through how to do this in the next lecture, but bear with me for a second:

```dockerfile
FROM python:3.10
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:80", "main:app"]
```

This is a `Dockerfile`, a definition of how to create a Docker image. Once you have this file, you can ask Docker to create the Docker image. Then, after creating the Docker image, you can ask Docker to run it as a container.

In this `Dockerfile` you can see the first line: `FROM python:3.10`. This tells Docker to first download the `python:3.10` image (an image someone else already created), and once that image is created, run the following commands.

The following commands are specific to our use case, and do things like install requirements, copy our source code into the image, and tell Docker what command to run when we start a container from this image.

This separation between images and containers is interesting because once the image is created you can ship it across the internet and:

- Share it with other developers.
- Deploy it to servers.

Plus once you've downloaded the image (which can take a while), starting a container from it is almost instant since there's very little work to do.