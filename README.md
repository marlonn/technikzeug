# Technikzeug

### What is this?

This is the public documentation Technikzeugs, a tech-related weblog for personal use. It's running in a
lxc container on host Abraxas and uses mariadb, django, django rest framework and nginx. Based on rynnon-php, which was developed with procedural php, mariadb and apache.

### to do

- implement search with multiple keywords
- show article images
- link search view to detail view

### current frontends

- localhost/artikel/
- localhost/admin/ # django's admin site
- localhost/artikel/api/ # django rest framework's browsable api

### database

database: mysql (provided by package mariadb)

database name: phpmyadmin

database user: phpmyadmin

### database backup

```sh
mysqldump -u [username] -p [databasename] > database-backup.sql
```

### installing stuff

**nginx**

```sh
sudo service apache2 stop
sudo apt install nginx-common
sudo rm /etc/nginx/sites-enabled/default
sudo apt install nginx-core nginx
sudo service apache2 start
```

**python and django**

```sh
sudo apt install python3-pip
sudo apt install python3-venv
mkdir ~/site-dev
cd ~/site-dev
virtualenv virtualenv
. virtualenv/bin/activate
pip install --upgrade pip
pip install "django==3.2.7" setuptools
django-admin.py startproject technikzeug .
```

add this to settings.py for database access:
```sh
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'phpmyadmin',
        'USER': 'phpmyadmin',
        'PASSWORD': '[password]',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}
```

`pip install mysqclient` keeps failing. This is what I've done, not quite sure what did the trick:
```sh
sudo ln -s /usr/local/mysql/bin/mysql_config /usr/bin/mysql_config
sudo apt install libmysqlclient-dev
(virtualenv) $ pip install --upgrade setuptools
(virtualenv) $ pip install mysqlclient
```

**inspectdb**

NOW begins the real fun! Let's try to use cyan's old database.

- https://docs.djangoproject.com/en/1.11/howto/legacy-databases/#auto-generate-the-models
- https://docs.djangoproject.com/en/1.11/ref/django-admin/#django-admin-inspectdb

```sh
./manage.py inspectdb artikel > models.py
./manage.py startapp artikel
mv models.py artikel/models.py
# ./manage.py manage.py migrate # i think this doesn't work with inspectdb
./manage.py createsuperuser
Username: admin
Email address: [admin email]
Password: [admin password]

# actually, it seems the initial migrations have to be done differently if the
# database already exists:
./manage.py makemigrations artikel
./manage.py migrate --fake artikel
# now make a "real" migration; i did a data migration to deal with html escaping
./manage.py makemigrations --empty artikel
./manage.py migrate

```

Register model in admin: https://docs.djangoproject.com/en/1.11/intro/tutorial02/#make-the-poll-app-modifiable-in-the-admin

Now, we can start the development server and browse the database content at localhost/admin:
```sh
sudo virtualenv/bin/python3 manage.py runserver 0:80
firefox 10.98.288.35/admin
```

### git setup (bitbucket)

```sh
cd ~/site-dev
git remote add origin git@bitbucket.org:marneu/technikzeugs.git
git config --global user.name "marneu"
git config --global user.email "marlon_neumann@gmx.de"
ssh-keygen -t rsa -b 4096 -C "marlon_neumann@gmx.de"
cat ~/.ssh/id_rsa.pub
# copy+paste here: https://bitbucket.org/account/user/marneu/ssh-keys/
ssh -T git@bitbucket.org # to verify
git push -u origin master
```

### sass

```sh
# used to use the ruby version, but since I'm planning to use React, might as well install those hundreds of node modules
sudo apt install --no-install-recommends npm
sudo npm install --global n
sudo n 14
PATH="$PATH"
sudo npm install --global sass
# let's try sass:
cd artikel/static/artikel
sass --watch style.sass style.css
```

### example request to api

```sh
http http://10.98.228.35/artikel/api/416/?json

http -a marneu:[marneu password] POST http://10.98.228.35/artikel/api/ titel="cli-test" text="testestetsetset" tags="test" datum="2021-03-13"
```

### executing migration from commits 8bae1c6 and 676dbf5

```bash
. .virtualenv/bin/activate
./manage.py migrate
# migration 003 works, 004 fails
./manage.py shell
# do things outlined in manual_migration.txt, then
./manage.py migrate
# migration 004 works
```

### production mode setup

- http://10.98.228.35/artikel/354/
- https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html#make-uwsgi-startup-when-the-system-boots
- https://vpsfix.com/community/server-administration/no-etc-rc-local-file-on-ubuntu-18-04-heres-what-to-do/

```sh
# static content
cd /home/ubuntu/site-dev 
mkdir static
virtualenv/bin/python3 manage.py collectstatic

# uwsgi
sudo pip install uwsgi
sudo cp etc-rc.local /etc/rc.local
sudo chmod +x /etc/rc.local

# nginx 
sudo cp technikzeug_nginx.conf /etc/nginx/sites-available/technikzeug
sudo ln -s /etc/nginx/sites-available/technikzeug /etc/nginx/sites-enabled/technikzeug

# os-container doesn't shut down normally anymore, probably because of uwsgi being started through /etc/rc.local
lxc restart django-cyan --force

# site should now be available at 10.98.228.35/artikel/ (internal ip)
```

**pull in changes from dev server**
```sh
git pull
# might have to change urls in some files, e.g. api-url in search.js
virtualenv/bin/python3 manage.py collectstatic
sudo service nginx restart

### start dev-server

The development server has to be started manually.
```bash
su ubuntu
cd /home/ubuntu/site-dev
# The new js-functions would have to be rewritten if runserver used port 8000.
# Have to use sudo to use port 80
sudo virtualenv/bin/python3 manage.py runserver --settings=technikzeug.settings_debug 0:80
```
