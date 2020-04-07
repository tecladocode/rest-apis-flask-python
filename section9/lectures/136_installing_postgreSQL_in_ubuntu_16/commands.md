## Install PostreSQL on Ubuntu 16.04

While logged in as root user:

```bash
apt-get update
apt-get install postgresql postgresql-contrib
```

After installation, change user to postgres user by running
```bash
sudo -i -u postgres
```

Connect to the database by running

```bash
psql
```

To exit postgres database console, run

```bash
\q
```

To exit postgres user
```bash
exit
```
