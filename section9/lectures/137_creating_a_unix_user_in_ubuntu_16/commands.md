## Create a user in Ubuntu 16.04
To create a new user, run the following command and enter the user details as prompted (password, full name etc). Remember to replace "jose" with the name of your user.


```bash
adduser jose
```

### Add the new user to sudo users

Running the visudo command will open a file (normally located at /etc/sudoers). 
```bash
visudo
```

Under "User privilege specification", add the following line below root line

```bash
jose ALL=(ALL:ALL) ALL
```

Save the file with CNTR+O and press enter to save it. Then CNTR+X to exit the file.

### To enable logging in to the server as the newly created user, enable password login to the server by running

```bash
vi /etc/ssh/sshd_config
```

This opens another file. To disable root login with password, change the following line. Note you need to press "i" key to go to insert/edit mode before changing the contents of the file.

```bash
PermitRootLogin yes
```

to 

```bash
PermitRootLogin no
```

Scroll down to the end of the file and add the following line

```bash
AllowUsers jose
```


To exit edit/insert mode, press escape key then ":" followed by wq and press enter. "wq" writes the file to disc and quits the file.

Finally, run

```bash
service sshd reload
```


