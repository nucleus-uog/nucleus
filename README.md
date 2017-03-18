# Nucleus
[![build status](https://gitlab.com/devine-industries/nucleus/badges/master/build.svg)](https://gitlab.com/devine-industries/nucleus/commits/master)
[![coverage report](https://gitlab.com/devine-industries/nucleus/badges/master/coverage.svg)](https://gitlab.com/devine-industries/nucleus/commits/master)

This project contains the Nucleus application for Web App Development 2 Group Project at University of Glasgow.
tests used within the primary Nucleus application.

The application provides automated testing for students completing the Tango with Django project in the first part of the course.

# How do I get this working?
## Docker (recommended)
Firstly, to install Docker to your system, follow the guides on the [Docker website](https://www.docker.com/products/overview).

Windows users without Hyper-V (Windows 10 Home users) will need to run the unsupported [Docker Toolbox](https://www.docker.com/products/docker-toolbox) rather than the new [Docker for Windows](https://docs.docker.com/docker-for-windows/) - the application should still work but will have to be run within the Docker Toolbox VM.

There are then two ways to run the application with Docker - using [the supplied docker-compose.yml](docker-compose.yml) (recommended) or manually - we'll only cover using the [docker-compose.yml](docker-compose.yml) method in this guide.

In order to get started, download the [docker-compose.yml](docker-compose.yml) file and the [nucleus.env.example](nucleus.env.example) file and keep them in the same folder.

Make a copy of the `nucleus.env.example` file and name it `nucleus.env`. Then, edit the file and set the variables correctly according to the comments in the file.

Once properly configured, run the following:

```
$ docker login registry.gitlab.com
$ docker-compose up -d
$ docker-compose exec web python manage.py migrate
$ docker-compose scale worker=6
$ docker-compose logs
```

This will first prompt to login to GitLab's registries, you'll need to log in using the same values you set `NUCLEUS_REGISTRY_USERNAME` and `NUCLEUS_REGISTRY_PASSWORD` to.

Then, this will download and run the containers, as configured in the `docker-compose.yml` file. After this, we run the migrate command within the web container to create the database tables defined by the application.

Next, we scale the worker container up to 6 containers - this means there are many more workers available to handle websockets and running the tests.

Finally, we view the logs of all of the running containers. You should then be able to visit `localhost:8000` to see the running application.

### Docker for Windows

If using Docker for Windows, you'll need to modify the Docker daemon settings to run using a TCP connection rather than a named pipe, this is required as the Linux application container is unable to use named pipes.

This can be done by modifying `%ProgramData%\docker\config\daemon.json` and adding (or modifying if the key exists) the following:

```json
{
    "hosts": ["tcp://127.0.0.1:2376", "npipe://"]
}
```

You can then restart the Docker for Windows application. This can be verified by running the following:

```
$ docker -H npipe:////./pipe/docker_engine info
$ docker -H tcp://127.0.0.1:2376 info
```

You can then set the `DOCKER_HOST` variable in `nucleus.env` as follows:

```
DOCKER_HOST=tcp://127.0.0.1:2376
```

You will also have to expose the port to the container so that the application can see the host Docker daemon.

### Docker Toolbox
If using Docker Toolbox, you are already using a TCP connection, and therefore will need to set the `DOCKER_HOST` variable as below:

```
DOCKER_HOST=tcp://127.0.0.1:<port>
```

Replacing the `<port>` with the port used by Docker Toolbox. This will typically be shown in the information printed when the Docker Toolbox console is started.

### Docker on Linux
If using Docker on a Linux system, you will likely have Docker set to use `/var/run/docker.sock`, add this as a volume to the same path in the container, and then set `DOCKER_HOST` in `nucleus.env` to the path.

```
DOCKER_HOST=unix:///var/run/docker.sock
```

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

This manual method assumes that Docker, Docker for Windows or Docker Toolbox is properly set up and configured. If this is the case, then the `docker.from_env()` call in [routes.py](rango/routes.py) will run successfully and be able to connect to your local Docker daemon.

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

# How does this all work?
Coming soon.

# How do I run the test task?
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

From the frontend, a websocket connection can be created to `/` from a logged in user, this connection will then get updates on the status of any job for that student.

```javascript
socket = new WebSocket("ws://" + window.location.host);
socket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    // data['status'] => Running
    // data['message'] => Cloning repo..
}
```

## Using Redis
If you wish to run the tasks with redis as a backend instead of in-memory, you must first install Redis - for Linux and Mac systems, follow the instructions on [the Redis website](https://redis.io/download); on Windows machines, install from [the MSOpenTech repository](https://github.com/MSOpenTech/redis/releases).

Then, switch `CHANNEL_LAYERS` configuration in [the settings module](nucleus/settings.py). You can view an example configuration in [the production_settings module](nucleus_production_settings.py).

Then, when running the application, you'll also need to run some workers. In different terminals, run `python manage.py runserver` once and `python manage.py runworker` many times.

You'll need to set the registry environment variables on every terminal.

You can also run workers to handle specific channels, for example, run `python manage.py runserver` once and also run `python manage.py runworker`, `python manage.py runworker --include-channels=run-tests` and `python manage.py runworker --include-channels=websockets.*`.

Using Redis will improve the performance of some of the application's realtime functionality - the application will struggle to send messages back during the test run if not using Redis.
