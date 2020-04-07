## Set up New User with PostgreSQL Permissions
This section assumes you created a new unix user in Ubuntu 16.04 (instructions in the previous lecture) and you are logged into the server as the new user.

To become the postgres user, run

```bash
sudo su
sudo -i -u postgres
```

To create a postgres user, run the following command. Note, the user must have the same name as the unix user logged into the server ("jose" in our case).

```bash
createuser jose -P
```

You will prompted twice to set the password for the new postgres user.

To create a database, run

```bash
createdb jose
```

To enforce password login to PostgreSQL with user jose, run the following commands. Note 9.5 is the PostgreSQL version installed in your server. Later this version may change so make sure to change your accordingly.

```bash
vi /etc/postgresql/9.5/main/pg_hba.conf
```

Scroll down to the bottom and change "peer" to "md5" in the following line under '# "local" is for unix domain socket connections only comment'. This is how the line should look after changing.

```bash
local all all md5
```

Finally, write and quit.
