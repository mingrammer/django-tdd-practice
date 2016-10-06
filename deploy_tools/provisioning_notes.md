New site provisioning

=====================

## Required packages

* nginx
* Python 3
* Git
* pip
* virtualenv

Running example on Ubuntu :
    sudo apt-get install nginx git python3 python3-pip
    sudo pip3 install virtualenv

## Setting Nginx virtual host

* Reference nginx.template.conf
* Replace the SITENAME with staging.my-domain.com

## Upstart Job

* Reference gunicorn-upstart.template.conf
* Replace the SITENAME with stating.my-domain.com

## Directory structure :
Assume the user home folder is '/home/username'

/home/username
|
----sites
    |
    ---- SITENAME
	 |
	 ---- database
	 ---- source
         ---- static
         ---- virtualenv

