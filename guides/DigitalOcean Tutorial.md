# Overview

This is a tutorial on deploying our sample app onto DigitalOcean, a cloud computing platform. We will walk through whole process from creating an account to setting up a server instance and running your app on it. The process should be similar for any cloud computing services, more specifically, once you set up your server on any platform of your choice, the remaining deploying steps should be identical. So this tutorial may serve as a general guide on deploying your python app onto any hosting platforms.

## Quick links
If you are a first time learner, we do encourage you to go through the whole tutorial. However, if you are just looking for help on a specific task, here are the links to the sections you may want to refer to:
- [DigitalOcean set-up]()
- [App deployment (applies to any hosting platform)]()
  - [Creating a user]()
  - [PostgreSQL user configuration]()
  - [Setting up nginx]()
  - [Setting up uWSGI]()

# DigitalOcean
## Introduction

DigitalOcean is a cloud infrastructure provider focused on simplifying web infrastructure for software developers. Basically, it allows you to rent servers with different performance at different cost. For more detailed information, you may refer to the official website help page [here](https://www.digitalocean.com/help/).

## Creating an account

In this tutorial, we'll be offering you a $10 coupon, which can cover the cost of the most basic tier of server for 2 months. And of course you may choose to use it for higher tiers but for a shorter period. Simply click this link to create your account to get the $10 coupon: [https://m.do.co/c/d54c088544ed](https://m.do.co/c/d54c088544ed). If the link doesn't work, simply paste it into your browser.

![Create an account](assets/DigitalOcean/create_account.png =200x200)

After clicking the link, you should be seeing a page like above. Simply create your account at the left-bottom corner and you'll receive the $10 coupon automatically. Beware that you'll be asked to provide payment info when creating the account, since all services (you chose) in DigitalOcean will be charged.

## Creating a Droplet

A server instance in DigitalOcean is called a `Droplet`. It's just a name that may vary in different platforms, for example, `Dyno` for Heroku and `EC2` for Amazon Web Service (AWS). Below are the simple steps to create a `Droplet`.

### Choosing an image

To create a `Droplet`, we must first specify an image, that is, choosing what Operating System you want for the server. We recommend to use Ubuntu LTS (Long Term Support) distribution. For more info on Ubuntu life time, please refer to the [official Ubuntu end of life page here](https://www.ubuntu.com/info/release-end-of-life). In our example, we'll use `Ubuntu 16.04.* x64`, which is a LTS distribution.

### Choosing a size

Next, we need to choose the specs for our server. In this tutorial, we'll be using the most basic tier of a Standard `Droplet`, which offers a single CPU with 512MB RAM, 20GB SSD and 1000 GB transfer at $5 per month. Generally, it's more than enough for testing personal applications, you may also run several services at a single Droplet.

### Choosing a datacenter region

Generally, choosing a region that's closest to your users will make your service deliver faster.

### Other configurations

In our example, we do not need to add any other services such as block storage or private network. So we will ignore these settings to keep our setting up simple and cheap. You may choose to use your own SSH key or you can just leave it unchecked and a password will be generated for you. At last, you may change the name of your `Droplet` to something you like and then click Create to create and launch your `Droplet`.

## Connecting to our droplet

<img src='access-consle' width=300>

Once you've created your `Droplet`, you will receive an email containing your login (`root`) and initial password for it. Now click the "Access Console" option in the dropdown menu associated with your `Droplet` as shown in above picture.

### Change your password

Now you will be prompt a console connected to your `Droplet`. Use the login `root` and the password received in your email to login. Then you will be ask to provide your password again and change it to a new password. Notice that all password field will not show any modification when you are typing, there is nothing wrong with your console, it's just a Ubuntu security feature. After changing your password, you are now logged in as the root user on your server.

If you have successfully followed the tutorial so far, then you have finished all the setting-ups that are specific to DigitalOcean. The following sections can serve as a standalone tutorial and can be applied to deployment onto any other platforms as well.

# Deploying Applications Onto Our Server

## Connecting to our server

First, we need to SSH our server. Simply use the recommend:

```
ssh root@<your server ip>
```

and you will be asked for the root password. Beware that `SSH` command only works on Mac, not on windows. However, there are plenty of softwares that you can use to SSH from windows, `putty` is one popular option.

## Installing required packages

After connecting to our server and logged in as root user, it is recommended to run the command

```
apt-get update
```

first to get all the available updates. Then we use the following command to install our required packages:

```
apt-get install postgresql postgresql-contrib
```

## Creating another user

Since the `root` user is the most powerful, we may want to limit access to it to improve security. So in this section, we will create a new user and config it to "act like" a `root` user but with certain limitation. And we will be logging as this user from now on. It is highly recommended to do so, but if you choose not to follow and simply want to login as the `root` user nonetheless, you may click [here to skip to the next section](lin_to_next_section).

### Hello John Doe

In this section, we will create a user named `johndoe`. You may choose any name you want, just remember to swap `johndoe` with your username for each command. We create a new user `johndoe` with the following command:

```
adduser johndow
```

You will be asked to enter and retype the password for this user, and then provide some info about this user. Notice that you can leave the info sections blank if you want to. And if you *managed* to enter unmatching passwords, simply proceed to complete the info section and we can set up the password later by using command:

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

and we need to add a new line for our user in this section:

```
# User privilege specification
root ALL=(ALL:ALL) ALL
johndoe ALL=(ALL:ALL) ALL
```

Remember that the `ALL` has to be ***all-caps***, otherwise it will raise syntax error.

After finishing adding this line, we use `ctrl + o` to save and press `ENTER` to overwrite, then we press `ctrl + x` to quit.

### Enable SSH for our new user

Next, we want to allow us to login as `johndoe` using SSH, and we may also want to disable login as `root` from SSH to make our server more secure. To do this, simply use the command:

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
# You may add some description here
AllowUsers johndoe
```

Next, press `Esc` to quit insert mode, press `:` (column) to enable the command function and enter `wq` to write and quit. Finally, we use the command:

```
service sshd reload
```

to enable our modifications.

Now we've created a new user `johndoe`, given it temporary super user privilege and enabled SSH for this user. Next, we'll be learning to link this user to our PostgreSQL database.

## Configuring our user for PostgreSQL

Since PostgreSQL allows its own user to interact with the database, we will need to create an according user and configure it to access the database.

### Creating a PostgreSQL user

We use the following command to create the user:

```
sudo -i -u postgres
createuser johndoe -P
```

After inputing and confirming the password, we now have created a Postgres user. Notice that we use the same username `johndoe` to create the PostgreSQL user, since by default, Postgres only allows the unix user with the same name as its Postgres user to interact with it.

### Creating a PostgreSQL database for our user

After having created the Postgres user, we use the command

```
createdb johndoe
```
 to create a database also name `johndoe`. And now we will explain the reason behind all these names.

 In Postgres, it allows a user to connect to the database with the same name by default, that is the Postgres `johndoe` user can always access the database named `johndoe`. And by default, Postgres only allows the unix user with the same name as its Postgres user to interact with it.

 So now, our unix user `johndoe` can directly interact with the PostgreSQL database named `johndoe` using command

 ```
 psql
 ```

 Also, here are some useful Postgres commands:

 To ouput the current connection info, use:
 ```
 \conninfo
 ```

 To quit Postgres:

 ```
 \q
 ```

### Improve security on our PostgreSQL database

However, we may notice that we've created a password for the Postgres user but never have to use it just because we used the same username in unix and Postgres. It is not really safe, so let's fix it. Use the below command to configure Postgres security options.

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

We change the line

```
local   all             all                                     peer
```

to

```
local   all             all                                     md5
```

to enable password authentication.

*** important: *** SQLAlchemy will ***NOT*** work unless we do this modification.

## Setting up nginx

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

Remember that the second line is just a precaution, it should be added already, but we don't want to get blocked out of the server!

At last, if the UFW (Ubuntu Firewall) is inactive, use the command below to activate it:

```
sudo ufw enable
```




## Setting up uWSGI
