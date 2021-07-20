
# Gestion Immo

real estate management website

# How to setup the project

## Clone the repository

Use the command `git clone https://github.com/honorezemagho/gestionimmo.git`

after you can use the command `cd gestionimmo` to navigate to your local version of repository.

## Create virtual environment for your work

use the command `virtualenv env --no-site-packages` 
and after `source env/bin/activate` (this one works only on linux)

## Install dependencies

use the command `pip install -r requirements.txt` to install project dependencies

## Database configuration (postgres)

use the command `cp .env.example .env` to create an environment file.
After use update the variables `DB_USER=your_postgres_user`,
`DB_PASSWORD=your_postgres_user_password` and `DB_HOST=your_posgres_host` by default it's `localhost`

## Migrations , Create superuser and run the server

use the command `python manage.py migrate` to migrate the database schema into yours.
use the command `python manage.py createsuperuser` to create a super user that we are going to use for the django admin.
To run the server we use the command `python manage.py runserver`.

## Assumptions

posgres is PostgreSQL

## Some useful resources

[Python cheatset](https://www.pythoncheatsheet.org/)\
[Python cheatset site(websitesetup)](https://websitesetup.org/python-cheat-sheet/)\
[Programiz python](https://www.programiz.com/python-programming/tutorial)\
[Django Central](https://djangocentral.com/) \
[Real Python](https://realpython.com/tutorials/django/) \
[Geeks For Geeks](https://www.geeksforgeeks.org/django-tutorial/)\
[Mozilla Developers Network](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django)\
