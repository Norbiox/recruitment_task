# recruitment_task
Solution for recruitment task.


## Prerequisites

* python 3.7
* Docker
* docker-compose


## How to run

First go to [omdbapi.com](http://www.omdbapi.com/apikey.aspx) and get free or paid API key.

Clone this repository and `cd` to it's folder. Create necessary environment variables:

* MYSQL_DATABASE (name of database that will be used)
* MYSQL_USER (name of database user)
* MYSQL_PASSWORD (password to the database)
* MYSQL_ROOT_PASSWORD (root password to mysql database)
* OMBDAPIKEY (your omdb API key)
* SECRET_KEY (secret key of django application)

Use docker-compose to build and run docker hosted application:

    docker-compose build
    docker-compose up -d

Voila! You can test API at (http://0.0.0.0:8000/).
