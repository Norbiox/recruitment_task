# recruitment_task
Solution for recruitment task.


## Description

This repository contains application that is solution for reqruitment task.
Task is described in [task_description.md](https://github.com/Norbiox/recruitment_task/blob/master/task_description.md).

As a solution django application was created, dockerized and deployed on Heroku.
Default database is `postgresql`, because it's available on Heroku.
Application is served by `gunicorn`, because of it's simplicity and reliability.
To fetch data from [OMDb API](http://www.omdbapi.com/) application uses `omdb` package.


## Prerequisites

* python 3.7
* Docker
* docker-compose


## Setup development environment

First go to [omdbapi.com](http://www.omdbapi.com/apikey.aspx) and get free or paid API key.

Clone this repository and `cd` to it's folder. Create necessary environment variables:

* POSTGRES_DB (name of database that will be used)
* POSTGRES_USER (name of database user)
* POSTGRES_PASSWORD (password to the database)
* OMBDAPIKEY (your omdb API key)
* SECRET_KEY (secret key of django application)
* DEBUG_VALUE (set non-empty string to turn DEBUG mode on)

Create `.env` file with database address:

    echo 'DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}"' > .env

Use docker-compose to build and run docker hosted application:

    docker-compose build
    docker-compose up -d

Voila! You can test API at (http://0.0.0.0:8000/).
