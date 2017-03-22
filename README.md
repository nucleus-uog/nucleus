# Nucleus
[![build status](https://gitlab.com/devine-industries/nucleus/badges/master/build.svg)](https://gitlab.com/devine-industries/nucleus/commits/master)
[![coverage report](https://gitlab.com/devine-industries/nucleus/badges/master/coverage.svg)](https://gitlab.com/devine-industries/nucleus/commits/master)

This project contains the Nucleus application for Web App Development 2 Group Project at University of Glasgow. The application provides automated testing for students completing the Tango with Django project in the first part of the course.

# Quick Start
## Docker (recommended)
1. Install [Docker Compose](https://docs.docker.com/compose/install/). If using Windows, Docker for Windows must be used - the application does not work on the unsupported Docker Toolbox as it does not support the most recent - version 3 - compose file format.
2. Download [docker-compose.yml](docker-compose.yml) and the [nucleus.env.example](nucleus.env.example) files.
3. Rename `nucleus.env.example` to `nucleus.env`.
4. Edit the configuration in `nucleus.env`, following the instructions in the comments.
5. Run `docker login registry.gitlab.com`, providing your GitLab login details (this may include a personal access token).
6. Run `docker-compose up -d` - this will download the containers from the official Docker registry and from the GitLab registry and start them, you'll be able to visit the application at `localhost:8000`.
7. Run `docker-compose exec web python3 manage.py makemigrations nucleus_app` to create the migrations for the application.
8. Run `docker-compose exec web python3 manage.py migrate`, this will create the tables in the MariaDB database. You may have to wait a moment to run this command for the database container to start up.
9. Run `docker-compose exec web python3 populate_nucleus.py` to populate the database with sample data.
10. Run `docker-compose exec web python3 manage.py createsuperuser` to create your admin user in the application.
11. Run `docker-compose scale worker=6` to scale the test worker to six containers.
12. Run `docker-compose scale http_worker=2` to scale the http worker to two containers.
13. Run `docker-compose logs -f` to view the logs for the application.
14. When finished, you can run `docker-compose down` to kill the containers.

### Notes
- Any emails that the application would send are printed to the console. When testing the reset password, check there.
- Docker Compose is configured to set up volumes for storing the MySQL database and the results (so they can be read by the application), you can check and remove these volumes if necessary using `docker volume` and appropriate subcommands.

## Manual
If you opt to run this manually, you'll need the following installed:

* [Python 3](http://python.org/)
* [Node.js](https://nodejs.org/en/)
* [Docker](https://www.docker.com/products/overview) ([Docker Toolbox](https://www.docker.com/products/docker-toolbox) or [Docker for Windows](https://docs.docker.com/docker-for-windows/), if using Windows)

Firstly, clone the repository:

```
$ git clone git@gitlab.com:devine-industries/nucleus.git
$ cd nucleus
```

Now, using npm, you'll need to install `gulp-cli`, as follows:

```
$ npm install -g gulp-cli
```

You'll also need to install the npm dependencies by running:

```
$ npm install
```

Then, it is recommended that you create a virtual environment to hold the Python dependencies:

**Linux:**
```
$ python -m venv venv
$ source venv/bin/activate
```

**Windows:**
```
$ python -m venv venv
$ venv\Scripts\activate.bat
```

Next, you'll want to install the Python depdendencies using pip into your virtual environment.

```
$ pip install -r requirements.txt
```

You'll need to set some environment variables so the application can login as your GitLab account and get the tests:

**Linux:**
```
$ export NUCLEUS_REGISTRY_USERNAME=<GitLab Username>
$ export NUCLEUS_REGISTRY_PASSWORD=<GitLab Password>
```

**Windows:**
```
$ set NUCLEUS_REGISTRY_USERNAME=<GitLab Username>
$ set NUCLEUS_REGISTRY_PASSWORD=<GitLab Password>
```

Finally, you can run the migrations then the application:

```
$ python manage.py migrate
$ python manage.py runserver
```

This manual method assumes that Docker, Docker for Windows or Docker Toolbox is properly set up and configured. If this is the case, then the `docker.from_env()` call in [routes.py](nucleus_app/routes.py) will run successfully and be able to connect to your local Docker daemon.

### TL;DR
```
$ git clone git@gitlab.com:devine-industries/nucleus.git
$ cd nucleus
$ npm install -g gulp-cli
$ npm install
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ export NUCLEUS_REGISTRY_USERNAME=<GitLab Username>
$ export NUCLEUS_REGISTRY_PASSWORD=<GitLab Password>
$ python manage.py migrate
$ python manage.py runserver
```


# How do I run the tests in the code?
In order to get the tests to run, create a `TestRun` instance with the repository url and student whose tests will run, as demonstrated below:

```python
run = TestRun(student=request.user,
              repository_url='https://github.com/davidtwco/uog-wad2.git')
run.save()
```

Then, one can send a message on the `test-run` channel with the id of the previously created run.

```python
Channel('run-tests').send({'id': run.id})
```

From the frontend, a websocket connection can be created to `/` from a logged in user, this connection will then get updates on the status of any job for that student. This is not currently used in the application and struggles if there aren't many workers available.

```javascript
socket = new WebSocket("ws://" + window.location.host);
socket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    // data['status'] => Running
    // data['message'] => Cloning repo..
}
```
