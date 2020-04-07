## Setting up Nginx
To install and cofigure Nginx on your server, follow the following instructions.

First, you need to update your server by running

```bash
sudo apt-get update
```

To install Nginx, run

```bash
sudo apt-get install nginx 
```

Allow Nginx access through firewall (otherwise incoming requests will be blocked by the firewall)

```bash
sudo ufw enable
sudo ufw allow 'Nginx HTTP'
```

Also since we have enabled firewall, remember to allow ssh through the firewall, else you will get locked out of the server.

```bash
sudo ufw allow ssh
```

You can check firewall status by using

```bash
sudo ufw status
```

To check Nginx status, use

```bash
systemctl status nginx
```

The following commands stop, start and restart Nginx respectively.

```bash
systemctl stop nginx
systemctl start nginx
systemctl restart nginx
```

### Configuring Nginx
Create a new file for the items REST API configuration.

```bash
sudo vi /etc/nginx/sites-available/items-rest.conf
```

Press "i" key (insert mode), copy and paste the following to the file

```bash
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
	location = 404.html {
		root /usr/share/nginx/html;
	}

	error_page 500 502  503 504 50x.html;
	location = /50x.html {
		root /usr/share/nginx/html;
	}
}
``` 

After writing and quiting the file (escape key then :wq enter) enable the configuration by running

```bash
sudo ln -s /etc/nginx/sites-available/items-rest.conf /etc/nginx/sites-enabled/
```

### Create the socket.sock file and clone the items rest app
Create a directory/folder for the app

```bash
sudo mkdir /var/www/html/items-rest
```

Since the director was created with root user, give access to the unix user ("jose" in our case) by making the user the owner of the directory.

```bash
sudo chown jose:jose /var/www/html/items-rest
```

Got to the directory, clone the app and install dependencies. Run the following commands one by one in that order.

```bash
cd /var/www/html/items-rest
git clone https://github.com/schoolofcode-me/stores-rest-api.git .
mkdir log
sudo apt-get install python-pip python3-dev libpq-dev
pip install virtualenv
virtualenv venv --python=python3.5
source venv/bin/activate
pip install -r requirements.txt 
```




