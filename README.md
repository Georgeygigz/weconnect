# Weconnect
Is a social media mock app with basic CRUD restful endpoints

## Requirements
- API keys from [Abstract](https://app.abstractapi.com/dashboard) API
## Setting the up locally
### Using Docker
- Ensure you have installed [docker](https://docs.docker.com/engine/install/) and [docker compose](https://docs.docker.com/compose/install/) on your local machine

- `git clone https://github.com/Georgeygigz/weconnect`
- `cd weconnect`
- `cp .env-sample-docker .env` to copy environment variables to .env file
- replace the .env variable with you correct variables
- If you have redis installed, you can stop it temporary
- `docker-compose build` to build docker image
- `docker-compose up` to run docker container
- visit [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/) to access the swagger documentation.


### Without Using Docker
- Ensure you have the following installed
    - [Python 3.8+](https://www.python.org/)
    - [Pipenv](https://pipenv.pypa.io/en/latest/)
    - [Redis](https://redis.io/)
    - [PostgreSQL](https://www.postgresql.org/)

- `git clone https://github.com/Georgeygigz/weconnect`
- `cd weconnect`
- `pipenv shell` to create and activate your virtual environment
- `pip install -r requirements` to install requirements
-  `cp .env_sample .env`  to copy environment variables to .env file
- ensure you have setup you postgres database
- replace the .env variable with you correct variables
-  `source .env` to source the env variables
-  `python3 manage.py migrate` to run migrations
- `python3 manage.py runserver` to start the server
- open a new console within the directory of your project and start the celery instance(while your environment is active) `celery -A app worker -l info`
- visit [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/) to access the swagger documentation.

### Run tests
- `pipenv run coverage run --source=app manage.py test --verbosity=2`
- get coverage report `pipenv run coverage report -m`


## Endpoints
- Signup user |POST| `http://127.0.0.1:8000/api/users/signup`
- Login user |POST| `http://127.0.0.1:8000/api/users/login`
- Verify user |GET| `http://127.0.0.1:8000/api/users/verify/{token}`
- Create post |POST| `http://127.0.0.1:8000/api/posts/`
- Get posts |GET| `http://127.0.0.1:8000/api/posts/`
- Get my posts |GET| `http://127.0.0.1:8000/api/posts/retrieve/myposts`
- Get single post |GET| `http://127.0.0.1:8000/api/posts/{id}`
- Update post |PATCH| `http://127.0.0.1:8000/api/posts/{id}`
- Delete post |DELETE| `http://127.0.0.1:8000/api/posts/{id}`
- Like post |GET| `http://127.0.0.1:8000/api/posts/like/{id}`


## Testing the endpoints
- Singup with a valid email, a verification email will be sent out to your email, click the link sent to your email and your account will be activated.
- If you don't get the verification email(and you did not use docker to set up your application), kindly check if your celery instance was started successfully.

- You need to be authenticated so as to access all endpoints apart from `login`, `listing all posts`, `listing single post` `signup`. To get authenticated, while on the swagger documentation, look for authorization button at the top right and insert the username and password.

## Tools used
- Celery for asynchronous processing
    - After users have signed up successfully a verification email is sent out to their email. This process is handled asynchronously.
    - We are also capturing user's geo-location data and holiday information. This service is making api calls to third party api, therefore, I have deployed celery to help in processing this request asynchronously.
- Redis as the message blocker
- Postgres is the most popular open source SQL server and integrates well with django
- [Tenacity](https://tenacity.readthedocs.io/en/latest/) for adding retry behavior. It is simple to use
- [Sendgrid](https://sendgrid.com/) as the mail host

## What I have not accomplished
- Due to pressing time requirements I have not manage to have all the necessary integrations
- This includes
    - CI pipeline using CircleCi
    - Codeclimate, to check the code quality
