# Process background tasks with the rq worker

We've got our queue and we've added tasks to it, but they won't run until we start consuming them and popping them off the queue.

To do this, we'll run a background worker whose job it is to pop items off the queue one at a time, and run the associated Python function with the associated arguments.

:::tip MacOS or Linux?
If you are using MacOS or Linux, you can run the background worker for testing using this command (make sure your virtual environment is active):

```bash
rq worker -u <insert your Redis url here> emails
```

The `rq` executable is available after installing the `rq` library with `pip`. The `-u` flag gives it the Redis URL to connect to. The `emails` at the end is the name of the queue that it should consume from. Make sure it matches the name of the queue you defined in `resources/user.py`.
:::

:::warning Running on MacOS
You may get an error when running `rq worker` directly using MacOS (without Docker):

```text
objc[21400]: +[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called.
```

If so, try running this command before starting your `rq worker`:

```bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

:::

The most reliable way to run the worker though, is using Docker.

We are already used to running our API using Docker, so now we can use the same Docker image to run our worker.

First, build the image:

```bash
docker build -t rest-apis-flask-smorest-rq .
```

Then run a container, but instead of running the default entrypoint (defined by the `CMD` line in the `Dockerfile`), we'll tell it to run the `rq` program:

```bash
docker run -w /app rest-apis-flask-smorest-rq sh -c "rq worker -u <insert your Redis url here> emails"
```

This ensures one of the [considerations](https://python-rq.org/docs/#considerations-for-jobs) that the `rq` documentation suggests: that the worker and the work generator (our API) share _exactly_ the same source code.

Run another Docker container for your API, and try to register!

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<div className="codeTabContainer">
<Tabs>
<TabItem value="app" label="Run the app" default>

```bash
docker run -p 5000:5000 rest-apis-flask-smorest-rq sh -c "flask run --host 0.0.0.0"
```

</TabItem>
<TabItem value="worker" label="Run the background worker">

```bash
docker run -w /app rest-apis-flask-smorest-rq sh -c "rq worker -u <insert your Redis url here> emails"
```

:::info
Make sure to enter your own Redis connection string in that command!
:::

</TabItem>
</Tabs>
</div>