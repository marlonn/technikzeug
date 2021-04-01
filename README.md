# django-cyan documentation

### What is this?

This is the public documentation for django-cyan, a virtualized Ubuntu server. It runs
as a lxd container on host Abraxas and serves a CRUD app using mysql, django
and nginx. Based on container "cyan" that runs the same content with procedural php
and apache.
Passwords and some usernames and email addresses are saved in a previous version of this document, renamed to "README_sensitive.md". It's still in the development server's project directory but purged from git.

### to do

- Suche mit mehreren Keywords implementieren (z.b. "enthält 'git' und 'python'"; momentan geht nur "enthält 'git python'")
- Bilder anzeigen
- in search-View auf detail-View verlinken

### current frontends

- localhost/artikel/
- localhost/admin/ # django's admin site
- localhost/artikel/api/ # drf's browsable api

### database

database: mysql (provided by package mariadb)

database name: phpmyadmin

### database backup

```bash
mysqldump -u [username] -p [databasename] > database-backup.sql
```

### installing stuff

**nginx**

ugh.

```bash
sudo service apache2 stop
sudo apt install nginx-common
sudo rm /etc/nginx/sites-enabled/default
sudo apt install nginx-core nginx
sudo service apache2 start
```

**snapd**

doesn't work at all, i guess because it has to run on debian stretch's
4.9 kernel? weird.

**python and django**

I used the official guide: https://docs.djangoproject.com/en/1.11/topics/install/

... and a bit of https://www.obeythetestinggoat.com/book/pre-requisite-installations.html

```bash
sudo apt install python3-pip
sudo apt install python3-venv
cd ~/site-dev
python3 -m venv virtualenv
. virtualenv/bin/activate
pip install --upgrade pip
pip install "django<1.12" setuptools
django-admin.py startproject technikzeug .
```

add this to settings.py for database access:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'phpmyadmin',
        'USER': '[username]',
        'PASSWORD': '[password]',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}
```

`pip install mysqclient` keeps failing. This is what I've done, not quite sure what did the trick:
```bash
sudo ln -s /usr/local/mysql/bin/mysql_config /usr/bin/mysql_config
sudo apt install libmysqlclient-dev
(virtualenv) $ pip install --upgrade setuptools
(virtualenv) $ pip install mysqlclient
```

**inspectdb**

NOW begins the real fun! Let's try to use cyan's old database.

- https://docs.djangoproject.com/en/1.11/howto/legacy-databases/#auto-generate-the-models
- https://docs.djangoproject.com/en/1.11/ref/django-admin/#django-admin-inspectdb

```bash
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
```bash
sudo virtualenv/bin/python3 manage.py runserver 0.0.0.0:80
firefox 10.98.288.35/admin
```

### git setup (bitbucket)

```bash
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

```bash
sudo apt --no-install-recommends ruby ruby-dev build-essentials
sudo gem install sass --no-user-install
```

### example request to api

http http://10.98.228.35/artikel/api/416/?json

http -a marneu:[marneu password] POST http://10.98.228.35/artikel/api/ titel="cli-test" text="testestetsetset" tags="test" datum="2021-03-13"


### executing migration from commits 8bae1c6 and 676dbf5

```bash
virtualenv/bin/python3 manage.py migrate
# migration 003 works, 004 fails
virtualenv/bin/python3 manage.py shell
# do things outlined in manual_migration.txt
virtualenv/bin/python3 manage.py migrate
# migration 004 works
```

### production mode setup

- http://10.98.228.35/artikel/354/
- https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html#make-uwsgi-startup-when-the-system-boots
- https://vpsfix.com/community/server-administration/no-etc-rc-local-file-on-ubuntu-18-04-heres-what-to-do/
```bash
# static content
cd /home/ubuntu/site-dev 
mkdir static
virtualenv/bin/python3 manage.py collectstatic
# os-container doesn't shut down normally anymore, probably because of uwsgi being started through /etc/rc.local
lxc restart django-cyan --force
```
