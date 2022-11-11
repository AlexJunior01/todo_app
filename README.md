# Todo App

## Objective
The objective of this project is to develop a REST API using the FastAPI framework to better understand concepts
such as ORM, service containerization and learn in practice some new concepts such as authentication.

## Description
This is an API of an ToDo app, which allows you to list, create, update, delete tasks and organize them into projects.

## Tecnologies
The project was developed using Python 3.9, PostgreSQL and use these libs and tools:
- **FastAPI** as framework;
- **Alembic** as migration system;
- **Pydantic** and **sqlachemy** to handle the API data validation and  use ORM model to comunicate with database;
- **Pytest** and **coverage** to tests.

## How to run

### Prerequisites
Before starting you need to have installed the following tools:
- [Git](https://git-scm.com) (Optional, you may want to manually download the project)
- [Docker Compose](https://docs.docker.com/compose/)

### Start up service
Start by cloning the repository or downloading the code, move to the project's directory and run this command:

``` shell
$ docker-compose up

# Or add the flag -d to run the service in the background
$ docker-compose up -d
```

So the API will start on `http://localhost:8000`, you can try the routes via Swagger on route /docs and 
see the documentation on /redoc.

## Tests
Tests can be run with the commands below:

``` shell
$ docker exec todo-api coverage run -m pytest

# Show the report and lists the lines that are not covered
$ docker exec todo-api coverage report -m

# Generate an HTML report in htmlcov/index.html
$ docker exec todo-api coverage html
```
