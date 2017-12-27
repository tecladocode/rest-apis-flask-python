# Overview

This is a tutorial on deploying our app onto DigitalOcean, a cloud computing platform. We will walk through whole process from creating an account to setting up a server instance and running your app on it. The process should be similar for any cloud computing services. Once you set up your server on any platform of your choice the remaining deploying steps should be identical. This tutorial may serve as a general guide on deploying your Python app onto any hosting platforms.

## Quick links

If you are a first time learner, we do encourage you to go through the whole tutorial. However, if you are just looking for help on a specific task, here are the links to the sections you may want to refer to:

- [DigitalOcean set-up](DigitalOcean%20Tutorial.md#digitalocean)
- [App deployment (applies to any hosting platform)](DigitalOcean%20Tutorial.md#deploying-applications-onto-our-server)
  - [Creating a unix user](DigitalOcean%20Tutorial.md#creating-another-user)
  - [Postgres configuration](DigitalOcean%20Tutorial.md#configuring-postgres)
  - [Setting up nginx](DigitalOcean%20Tutorial.md#nginx)
  - [Setting up uWSGI](DigitalOcean%20Tutorial.md#uwsgi)

# DigitalOcean
## Introduction

DigitalOcean is a cloud infrastructure provider focused on simplifying web infrastructure for software developers. It allows you to rent servers with different performance at different cost. For more detailed information, you may refer to the official website help page [here](https://www.digitalocean.com/help/).

## Creating an account

You can sign up to DigitalOcean using our affiliate link. Doing so gives you a starting credit of $10, which allows you to rent a server for 2 months. Click this link to create your account and get the $10: [https://m.do.co/c/d54c088544ed](https://m.do.co/c/d54c088544ed). If the link doesn't work, paste it into your browser. 

![Create an account](assets/DigitalOcean/create_account.png)

After clicking the link, you should see a page like the above. Create your account at the left-bottom corner and you'll receive the $10 automatically. Beware that you'll be asked to provide payment info when creating the account, since all services (which you'll choose below) in DigitalOcean will be charged after your credit runs out.

## Creating a Droplet

A server instance in DigitalOcean is called a `Droplet`. It's just a name that may vary in different platforms, for example, `Dyno` for Heroku and `EC2` for Amazon Web Service (AWS). Below are the simple steps to create a `Droplet`.

### Choosing an image

To create a `Droplet`, we must first specify an image, that is, choosing what Operating System you want for the server. We recommend to use an Ubuntu LTS (Long Term Support) distribution. For more info on Ubuntu life time, please refer to the [official Ubuntu end of life page here](https://www.ubuntu.com/info/release-end-of-life). In our example, we'll use `Ubuntu 16.04.* x64`, which is an LTS distribution.

### Choosing a size

Next, we need to choose the specs for our server. In this tutorial, we'll be using the most basic tier of a Standard `Droplet`, which offers a single CPU with 512MB RAM, 20GB SSD and 1000 GB transfer at $5 per month. Generally, it's more than enough for running personal applications. You may also run several services in a single Droplet.

### Choosing a datacenter region

Generally, choosing a region that's _closest to your users_ will make your service deliver faster. If your users are primarily in the United States, you could choose a United States-based Droplet.

### Other configurations

In our example, we do not need to add any other services such as block storage or private network. So we will ignore these settings to keep our setup simple and cheap. You may choose to use your own SSH key or you can just leave it unchecked and a password will be generated for you. At last, you may change the name of your `Droplet` to something you like and then click Create to create and launch your `Droplet`.

## Connecting to our droplet

![DigitalOcean Access Console](assets/DigitalOcean/access_console.png)

Once you've created your `Droplet`, you will receive an email containing your login (`root`) and initial password for it. Now click the "Access Console" option in the dropdown menu associated with your `Droplet` as shown in above image.

### Change your password

Now you will be shown a console connected to your `Droplet`. Use the login `root` and the password received in your email to login. Then you will be ask to provide your password again and change it to a new password. Notice that all password field will not show any modification when you are typing. There is nothing wrong with your console, it's just a Ubuntu security feature. After changing your password, you are now logged in as the root user on your server.

If you have successfully followed the tutorial so far, then you have finished all the setting-ups that are specific to DigitalOcean. The following sections can serve as a standalone tutorial and can be applied to deployment onto any other platforms as well.

# Deploying Applications Onto Our Server

## Connecting to our server

First, we need to SSH our server. Simply use the command:

```
ssh root@<your server ip>
```

You will be asked for the root password. Beware that `SSH` command only works on Unix, not on Windows. However, there are plenty of softwares that you can use to SSH from Windows, [PuTTy](http://www.putty.org/) is a popular choice.

## Installing required packages

After connecting to our server and logging in as the `root` user, it is recommended to run the below command first to get all the available updates:

```
apt-get update
```

Then we use the following command to install our required packages:

```
apt-get install postgresql postgresql-contrib
```

Note that this is a just an example to install different packages using one command, we may need more packages in the following sections.

## Creating another user

Since the `root` user is the most powerful, we may want to limit access to it to improve security. So in this section, we will create a new user and config it to "act like" a `root` user but with certain limitation. And we will be logging as this user from now on. It is highly recommended to do so, but if you choose not to follow and simply want to login as the `root` user anyway, you may click [here to skip to the next section](DigitalOcean%20Tutorial.md#configuring-postgres).

### Hello John Doe

In this section, we will create a user named `johndoe`. You may choose any name you want, just remember to swap `johndoe` with your username for each command. We create a new user `johndoe` with the following command:

```
adduser johndoe
```

You will be asked to enter and retype the password for this user, and then provide some info about this user. Notice that you can leave the info sections blank if you want to. And if you entered unmatching passwords, just complete the info section and we can change the password later by using the command:

```
passwd johndoe
```

### Providing user with additional privilege

Since we will be logging in as `johndoe` for most of the time in the future, we will want it to have some "extra power", that is, temporarily acting as a super user. To do this, we need to run the command:

```
visudo
```

first, and we will see a text file popping up. Then we navigate to the lines containing:

```
# User privilege specification
root ALL=(ALL:ALL) ALL
```

You can do this with the arrow keys. We need to add a new line for our user in this section:

```
# User privilege specification
root ALL=(ALL:ALL) ALL
johndoe ALL=(ALL:ALL) ALL
```

Remember that the `ALL` has to be **all uppercase**, otherwise it will raise syntax error.

After adding this line, use `ctrl + o` to save and press `ENTER` to overwrite, then press `ctrl + x` to quit.

### Enable SSH for our new user

Next, we want to allow us to login as `johndoe` using SSH, and we may also want to disable login as `root` from SSH to make our server more secure. To do this, use the command:

```
vi /etc/ssh/sshd_config
```

And we will be prompted with another text file. Navigate to the section which contains:

```
# Authentication
PermitRootLogin yes
```

Press `i` on your keyboard to enter insert mode and change the `yes` to `no` to disallow login as root. Then go to the bottom of the file and add the following lines:

```
AllowUsers johndoe
```

Next, press `Esc` to quit insert mode, press `:` (colon) to enable the command function and enter `wq` to write and quit. Finally, we use the command:

```
service sshd reload
```

to enable our modifications.

Now we've created a new user `johndoe` and enabled both its super user privilege and SSH access. Next, we'll be learning to link this user to our PostgreSQL database.

## Configuring Postgres

Postgres allows from the start a user to access a database with its own name. Thus we must:

1. Create a `johndoe` user inside PostgreSQL; and
2. Create a `johndoe` database in PostgreSQL.

Because we have a `johndoe` user in our server, it will automatically have permission to access the `johndoe` user in Postgres, and will be able to access the `johndoe` database.

### Installing PostgreSQL

```
apt-get install postgresql postgresql-contrib
```

### Creating a Postgres user

We use the following command to create the user:

```
sudo -i -u postgres
createuser johndoe -P
```

After inputing and confirming the password, we now have created a Postgres user. Remember that we use the same username `johndoe` to create the Postgres user, since by default, Postgres only allows the UNIX user with the same name as its Postgres user to interact with it.

### Creating a PostgreSQL database for our user

After having created the Postgres user, we use the command

```
createdb johndoe
```

to create a database also name `johndoe`. Now, our UNIX user `johndoe` can directly interact with the PostgreSQL database named `johndoe` using the command:

```
psql
```

### Some useful Postgres commands

To output the current connection info, use:

```
\conninfo
```

To quit Postgres:

```
\q
```

### Improve security on our PostgreSQL database

However, notice that we've created a password for the Postgres user but never have to use it just because we used the same username in UNIX and Postgres. It is safer to require a password. Use the below command to configure Postgres security options.

```
sudo vi /etc/postgresql/9.5/main/pg_hba.conf
```

Navigate to the bottom of the file, and we may see something like this:

```
# Database administrative login by Unix domain socket
local   all             postgres                                peer

# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     peer
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
```

Change the line

```
local   all             all                                     peer
```

to

```
local   all             all                                     md5
```

to enable password authentication.

**Important:** SQLAlchemy will ***NOT*** work unless we do this modification.

## Nginx

Nginx (engine x) is an HTTP and reverse proxy server, a mail proxy server, and a generic TCP/UDP proxy server. In this tutorial, we use nginx to direct traffic to our server. Nginx can be really helpful in scenarios like running our app on multiple threads, and it performs very well so we don't need to worry about it slowing down our app. More details about nginx can be found [here](https://nginx.org/en/).

### Installing nginx

```
sudo apt-get install nginx
```

### Configure firewall to grant access to nginx

First, check if the firewall is active:

```
sudo ufw status
```

If not, we will enable it later. Before that, let's add some new rules:

```
sudo ufw add 'Nginx HTTP'
sudo ufw add ssh
```

**Important:** the second line, adding SSH rules, is not related to nginx configuration, but since we're activating the firewall, we don't want to get blocked out of the server!

If the UFW (Ubuntu Firewall) is inactive, use the command below to activate it:

```
sudo ufw enable
```

To check if nginx is running, use the command:

```
systemctl status nginx
```

Some other helpful command options for system controller are:

```
systemctl start <service_name>
systemctl restart <service_name>
systemctl reload <service_name>
systemctl stop <service_name>
```

### Configure nginx for our app

Before deploying our app onto the server, we need to configure nginx for our app. Use the below command to create a config file for our app:

```
sudo vi /etc/nginx/sites-available/items-rest.conf
```

Note that `items-rest` is what we named our service, you may change it accordingly, but remember to remain consistent throughout the configurations.

Next, we input the below text into `items-rest.conf` file. **Remember to change your service name accordingly in this file as well**.

```nginx
server {
  listen 80;
  real_ip_header X-Forwarded-For;
  set_real_ip_from 127.0.0.1;
  server_name localhost;

  location / {
    include uwsgi_params;
    uwsgi_pass unix:/var/www/html/items-rest/socket.sock;
    uwsgi_modifier1 30;
  }

  error_page 404 /404.html;
  location = /404.html {
    root /usr/share/nginx/html;
  }

  error_page 500 502 503 504 /50x.html;
  location = /50x.html {
    root /usr/share/nginx/html;
  }
}
```

The above config allows nginx to send the request coming from our user's browser to our app. It also sets up some error pages for our service using nginx predefined pages.

And at last, in order to enable our configuration, we need to do something like this:

```
sudo ln -s /etc/nginx/sites-available/items-rest.conf /etc/nginx/sites-enabled/
```

### Setting up our app folder

First, we create a folder for our app:

```
sudo mkdir /var/www/html/items-rest
```

The folder is owned by the `root` user since we used `sudo` to create it. We need to transfer ownership to our current user:

```
sudo chown johndoe:johndoe /var/www/html/items-rest
```

Remember that `johndoe` is the username in our tutorial, make sure you change it to yours accordingly. The same goes for `items-rest`.

Next, we get our app from Git:

```
cd /var/www/html/items-rest/
git clone https://github.com/schoolofcode-me/stores-rest-api.git .
```

Note that there's a trailing space and period (` .`)at the end, which tells git the destination is the current folder. If you're not in this folder `/var/www/html/items-rest/`, remember to switch to it or explicitly specify it in the git command. And for the following commands in this section, we all assume that we are inside the folder `/var/www/html/items-rest/` unless specified otherwise.

In order to store logs, we need to create a log folder, (under `/var/www/html/items-rest/`):

```
mkdir log
```

Then we will install a bunch of tools we need to set up our app:

```
sudo apt-get install python-pip python3-dev libpq-dev
```

Next, to install `virtualenv`:

```
pip install virtualenv
```

After it is installed, we can create a `virtualenv`:

```
virtualenv venv --python==python3.5
```

Note that Ubuntu usually comes with `Python3.5` and it is what we used in the sample code, if you choose to use different version of Python, feel free to change it accordingly and it will be the Python version inside your `virtualenv`.

To activate `virtualenv`:

```
source venv/bin/activate
```

You should see `(venv)` appears at the start of your command line now. We assume that we are in `virtualenv` for all the following commands in this section unless specified otherwise.

Next, use the command below to install the specified dependencies:

```
pip install -r requirements.txt
```

`requirement.txt` is a text file that includes all the dependencies that we created in our Git folder. It's highly recommended to have a `requirements.txt` file with all libraries your project requires.

Next, let's set up uWSGI and finish deploying our app.

## uWSGI

We will be using uWSGI to run the app for us, in this way, we can run it in multiple threads within multiple processes. It also allow us to log more easily. More details on uWSGI can be found [here](https://uwsgi-docs.readthedocs.io/en/latest/).

First, we define a uWSGI service in the system by:

```
sudo vi /etc/systemd/system/uwsgi_items_rest.service
```

And the content we are going to input is shown below:

```
[Unit]
Description=uWSGI items rest

[Service]
Environment=DATABASE_URL=postgres://johndoe:<johndoe_postgres_password>@localhost:5432/johndoe
ExecStart=/var/www/html/items-rest/venv/bin/uwsgi --master --emperor /var/www/html/items-rest/uwsgi.ini --die-on-term --uid johndoe --gid johndoe --logto /var/www/html/items-rest/log/emperor.log
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

We will explain the basic idea of these configs. Each pair of square brackets `[]` defines a `section` which can contain some properties.

The `Unit` section simply provides some basic description and can be helpful when looking at the logs.

The `Service` section contains several properties related to our app. The `Environment` properties defines all the environment variables we need in our code. In our sample code, we want to retrieve the DATABASE_URL from system environment. And this is the place where you should keep all your secrets, such as secret keys and credentials. Beware that the `DATABASE_URL` should follow the format:

```
<database_type>://<db_username>:<db_user_password>@localhost:<db_port>/<db_name>
```

The `ExecStart` property informs uWSGI on how to run our app as well as log it.

At last, the `WantedBy` property in `Install` section allows the service to run as soon as the server boots up.

**Important:** remember to change the username, password, database name and service name/folder accordingly in your own code.

```
[uwsgi]
base = /var/www/html/items-rest
app = run
module = %(app)

home = %(base)/venv
pythonpath = %(base)

socket = %(base)/socket.sock

chmod-socket = 777

processes = 8

threads = 8

harakiri = 15

callable = app

logto = /var/www/html/items-rest/log/%n.log
```
