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

```sh
$ git clone git@gitlab.com:devine-industries/nucleus.git
$ cd nucleus
```

Now, using npm, you'll need to install `gulp-cli`, as follows:

```sh
$ npm install -g gulp-cli
```

You'll also need to install the npm dependencies by running:

```sh
$ npm install
```

Then, it is recommended that you create a virtual environment to hold the Python dependencies:

**Linux:**
```sh
$ python -m venv venv
$ venv/bin/activate
```

**Windows:**
```sh
$ python -m venv venv
$ venv\Scripts\activate.bat
```

Next, you'll want to install the Python depdendencies using pip into your virtual environment.

```sh
$ pip install -r requirements.txt
```

Finally, you can run the application:

```sh
$ python manage.py runserver
```

#### TL;DR
```sh
$ git clone git@gitlab.com:devine-industries/nucleus.git
$ cd nucleus
$ npm install -g gulp-cli
$ npm install
$ python -m venv venv
$ venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py runserver
```

## How does this all work?
Coming soon.

## How do I run the test task?
Coming soon.