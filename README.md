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

Use docker-compose to build, test and run docker hosted application:

    docker-compose build
    docker-compose up -d

Voila! You can test API at (http://0.0.0.0:8000/).


**NOTE**:

You can test and run application in your environment. All you need to do is to modify
`DATABASE_URL` in `.env` file by inserting there address of your working postgres database or default SQLite adress:

    sqlite:///db.sqlite3


## API documentation

**list movies**
----
  Returns all movies existing in database

* **URL**

  /movies

* **Method:**

  `GET`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[ [movie_object] ]`
 
* **Sample Call:**

  `curl "http://localhost:8000/movies"`


**fetch movie**
----
  Requests OMDb API for movie with given by user title and returns it.

* **URL**

  /movies

* **Method:**

  `POST`

* **Data Params**

    **Required:**

    `title=[string]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[movie_object]`
 
* **Error Response:**

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "omdbAPI key is invalid" }`

  OR

  * **Code:** 400 BADREQUEST <br />
    **Content:** `{ error : "'title' field is required" }`

* **Sample Call:**

  `curl -d "title=Shrek" -X POST "http://localhost:8000/movies"`


**list comments**
----
  Return comments assigned to movies.

* **URL**

  /comments

* **Method:**

  `GET`

*  **URL Params**

   **Optional:**
 
   `movieID=[integer]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[ {
        ID : [integer],
        Movie : [string],
        Text : [string],
        Created : [datetime_string]
    } ]`
 
* **Error Response:**

  * **Code:** 404 NOTFOUND <br />
    **Content:** `{ error : "Movie object has not been found" }`

* **Sample Call:**

  `curl "http://localhost:8000/comments?movieID=2"`


**add comment**
----
  Post comment to movie.

* **URL**

  /comments

* **Method:**

  `POST`

* **Data Params**

    **Required:**

    `movieID=[string]&text=[string]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
        ID : [integer],
        Movie : [string],
        Text : [string],
        Created : [datetime_string]
    }`
 
* **Error Response:**

  * **Code:** 404 NOTFOUND <br />
    **Content:** `{ error : "Movie object has not been found" }`

* **Sample Call:**

  `curl -d "movieID=1&text=asdas" -X POST "http://localhost:8000/comments`


**top**
----
  Returns ranking of most commented movies.
  Statistics are generated basing on specified date range.

* **URL**

  /top

* **Method:**

  `GET`

*  **URL Params**

   **Required:**
 
   `begin_date=[iso_date_string]`
   `end_date=[iso_date_string]`


* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[ {
        movie_id : [integer],
        total_comments : [integer],
        rank : [integer]
    } ]`
 
* **Sample Call:**

  `curl "http://localhost:8000/top?begin_date=2017-01-02&end_date=2018-11-23"`
