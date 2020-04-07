## Setting up uWSGI
This guide will help you set up uWSGI on your server to run the items rest app. Go to the items-rest directory we created in the previous lecture.

```bash
cd /var/www/html/items-rest
```

### Create Ubuntu service
Run the following command to create a service file.

```bash
sudo vi /etc/systemd/system/uwsgi_items_rest.service 
```

Copy and paste the following to the file. Note "jose:1234" is the username:password combination of the Postgres user we created before. Change yours accordingly. 

```bash
[Unit]
Description=uWSGI items rest

[Service]
Environment=DATABASE_URL=postgres://jose:1234@localhost:5432/jose
ExecStart=/var/www/html/items-rest/venv/bin/uwsgi --master --emperor /var/www/html/items-rest/uwsgi.ini --die-on-term --uid jose --gid jose --logto /var/www/html/items-rest/log/emperor.log
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

Replace the uwsgi.ini file contents with the following

```bash
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

Finally start the app by running

```bash
sudo systemctl start uwsgi_items_rest
```
