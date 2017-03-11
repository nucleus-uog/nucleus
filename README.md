# Nucleus
[![build status](https://gitlab.com/devine-industries/nucleus/badges/master/build.svg)](https://gitlab.com/devine-industries/nucleus/commits/master)
[![coverage report](https://gitlab.com/devine-industries/nucleus/badges/master/coverage.svg)](https://gitlab.com/devine-industries/nucleus/commits/master)

This project contains the Nucleus application for Web App Development 2 Group Project at University of Glasgow.
tests used within the primary Nucleus application. 

The application provides automated testing for students completing the Tango with Django project in the first part of the course.

## How do I get this working?
### Docker (recommended)
A guide on how to run this application using Docker will come later as the project nears completion.

To install Docker to your system, follow the guides on the [Docker website](https://www.docker.com/products/overview). Windows users without Hyper-V will need to run the unsupported [Docker Toolbox](https://www.docker.com/products/docker-toolbox) rather than the new [Docker for Windows](https://docs.docker.com/docker-for-windows/) - the application should still work.
### Manual
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

#### TL;DR
```
$ git clone git@gitlab.com:devine-industries/nucleus.git
$ cd nucleus
$ npm install -g gulp-cli
$ npm install
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver
```

## How does this all work?
Coming soon.

## How do I run the test task?
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

### Using Redis
If you wish to run the tasks with redis as a backend instead of in-memory, you must first install Redis - for Linux and Mac systems, follow the instructions on [the Redis website](https://redis.io/download); on Windows machines, install from [the MSOpenTech repository](https://github.com/MSOpenTech/redis/releases).

Then, switch `CHANNEL_LAYERS` configuration in [the settings module](nucleus/settings.py). There will be a commented configuration for Redis.

Then, when running the application, you'll also need to run some workers. In different terminals, run `python manage.py runserver` once and `python manage.py runworker` many times.

You'll need to set the registry environment variables on every terminal.

You can also run workers to handle specific channels, for example, run `python manage.py runserver` once and also run `python manage.py runworker`, `python manage.py runworker --include-channels=run-tests` and `python manage.py runworker --include-channels=websockets.*`.

Using Redis will improve the performance of some of the application's realtime functionality - the application will struggle to send messages back during the test run if not using Redis.