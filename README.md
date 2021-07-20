
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

## Assumptions

posgres is PostgreSQL
