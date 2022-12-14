# Articles navigator
A dockerized FastAPI App with 2 options of rendering (server-side and React frontend).
Provides the opportunity for users' articles navigation with standard user authentication system.
![App structure](image/app_diagram.png "App structure") 
____
PostgreSQL is used for collecting data about users and their articles, MongoDB is used for registrating events.
The rendering server has some additional functionality compared with the React frontend: it is connected with RabbitMQ and Sentry. 
RabbitMQ is used while the rendering server pushes message about a new registered user into a queue and the listening server listens to this queue.
Sentry is used for registrating server errors.
____

### CodeClimate and CI status
<a href="https://codeclimate.com/github/Dddarknight/articles-api/maintainability"><img src="https://api.codeclimate.com/v1/badges/9a422e0f9bb23c66c9a3/maintainability" /></a> <a href="https://codeclimate.com/github/Dddarknight/articles-api/test_coverage"><img src="https://api.codeclimate.com/v1/badges/9a422e0f9bb23c66c9a3/test_coverage" /></a> [![Python CI](https://github.com/Dddarknight/articles-api/actions/workflows/pyci.yml/badge.svg)](https://github.com/Dddarknight/articles-api/actions)

## Links
This project was built using these tools:
| Tool | Description |
|----------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | "Web framework for building APIs with Python" |
| [PostgreSQL](https://www.postgresql.org/) |  "An open source object-relational database system" |
| [SQLAlchemy](https://www.sqlalchemy.org/) |  "The Python SQL toolkit and Object Relational Mapper" |
| [Alembic](https://alembic.sqlalchemy.org/en/latest/) |  "A lightweight database migration tool for usage with the SQLAlchemy" |
| [MongoDB](https://www.mongodb.com/) |  "A NoSQL database program" |
| [React](https://reactjs.org/) |  "A JavaScript library for building user interfaces" |
| [RabbitMQ](https://www.rabbitmq.com/) | "An open source message broker" |
| [poetry](https://python-poetry.org/) |  "Python dependency management and packaging made easy" |
| [Py.Test](https://pytest.org) | "A mature full-featured Python testing tool" |
| [Sentry](https://sentry.io/welcome/) | "Application Monitoring and Error Tracking Software" |


## Installation
**Copy a project**
```
$ git clone git@github.com:Dddarknight/articles-api.git
$ cd articles-api 
```

**Set up environment variables**
``` 
$ touch .env

# You have to fill .env file. See .env.example.
# You will have to fill username and password fields for PostgreSQL, RabbitMQ, email (from this email messages will be sent to moderators). If you don't have these credentials, please follow the instructions in the official documentation.

# To get a SECRET_KEY for FastAPI run:
$ openssl rand -hex 32
```

**Set up environment variables for frontend**
```
$ cd frontend
$ touch .env
# Then you have to fill .env file in frontend for Firebase project configuration. See .env.example.
```

**Working with Docker**
```
$ cd ..

# If you haven't used Docker earlier, you should follow the installation instruction on the official website (https://docs.docker.com/engine/install/).
# Then:
$ sudo apt install docker-compose

$ docker-compose up -d --build
```

## Description and usage

**Functionality connected with users management**

| Page | Description |
|----------|---------|
| Sign-up |  First you need to register in the app using the provided form of registration. |
| Log in | Then you have to log in using the information you've filled in the registration form. JSON Web Tokens are used for authorization.  |
| Users | You can see list of all users on the relevant page. |
| User | The information about the user. The user's data can be changed or deleted only by the authorized user. |

**Functionality connected with articles management**

| Page | Description |
|----------|---------|
| Articles | Here you can see the list of users' articles. Also here you can create a new article. |
| Article | Only authorized user's article can be changed or deleted. |

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)