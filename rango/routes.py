import time
import os
import shutil
import json
from os.path import join, exists

from datetime import timedelta
import docker
from django.template.defaultfilters import slugify
from channels import Group
from channels.routing import route
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http

from .models import (
    TestRun,
    TestRunDetail,
    Test
)
from .exceptions import NucleusException


REPOSITORY = 'registry.gitlab.com/devine-industries/nucleus-tests'
TAG = 'latest'
CURRENT_DIRECTORY = os.getcwd()
# We keep track of the path in the regular Windows format for later.
OUTPUT_DIRECTORY_WIN = join(CURRENT_DIRECTORY, 'results')
# Docker expects our Windows paths to be in the form: /c/Users/Batman/...
OUTPUT_DIRECTORY_DOCKER = OUTPUT_DIRECTORY_WIN.replace('C:\\', '/c/').replace('\\', '/')
VOLUMES = {
    OUTPUT_DIRECTORY_DOCKER: {
        'bind': '/nucleus/results',
        'mode': 'rw'
    }
}


client = docker.from_env()


@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({'accept': True})
    _send_message(message.user.email, 'Connected', 'Socket connection established...');
    Group(slugify(message.user.email)).add(message.reply_channel)


@channel_session_user
def ws_disconnect(message):
    Group(slugify(message.user.email)).discard(message.reply_channel)


def run_tests(message):
    '''
    Runs the test suite and outputs the results
    in the results folder.

    You can run this as below, passing the
    id of a TestRun model instance.

    ```python
    from channels import Channel

    Channel('run-tests').send({
        'id': 2 # change to new instance id
    })
    ```
    '''
    # Try and load the test run model instance
    # that this was provided with.
    try:
        run = TestRun.objects.get(
            id=message.content.get('id'),
        )
    except TestRun.DoesNotExist:
        _send_message(message.user.email, 'Failed', ':: Could not find test run instance.');
        raise NucleusException('Test Run instance not found.')

    if run.status == 'Complete':
        _send_message(message.user.email, 'Complete', ':: Test Run already complete.');
        raise NucleusException('Started TestRun for a instance '
                               'that is already complete.')

    # Get details.
    student_email = run.student.email
    repository_url = run.repository_url

    # Send status to websocket.
    _send_message(student_email, 'Starting', ':: Loading test run details..')

    # Update status.
    run.status = 'Running'
    run.save()

    # Log the start time.
    start = time.time()

    # Set up our environment variables and
    # volumes for running the container.
    environment = {
        'TESTS_STUDENT': student_email,
        'TESTS_REPO_URL': repository_url
    }

    # Remove previous results
    _send_message(student_email, 'Running', ':: Removing previous results directory..')
    student_directory = join(OUTPUT_DIRECTORY_WIN, student_email)
    if exists(student_directory):
        shutil.rmtree(student_directory)

    # Send status to websocket.
    _send_message(student_email, 'Running', ':: Starting container...')

    # Run the container.
    image = client.images.pull(REPOSITORY, tag=TAG, auth_config={
        'username': os.environ['NUCLEUS_REGISTRY_USERNAME'],
        'password': os.environ['NUCLEUS_REGISTRY_PASSWORD']
    })
    container = client.containers.run(image.id, environment=environment,
                                      volumes=VOLUMES, detach=True)

    # As the logs come in, stream them back to the
    # listening websocket, if it exists.
    for line in container.logs(stream=True):
        _send_message(student_email, 'Running', line.decode('utf-8'))

    # Get the end time.
    end = time.time()

    # Update the details of the run instance
    # with the details from the container.
    run.log = container.logs()
    run.status = 'Running'
    run.test_version = 'N/A'
    run.time_taken = timedelta(seconds=end-start)
    run.save()

    # Send status to websocket.
    _send_message(student_email, 'Running', ':: Gathering results..')

    _collect_results(student_email, run)


def _collect_results(student_email, run):
    # Check if we can find the results directory for the student.
    _check_path(student_email=student_email,
                path=join(OUTPUT_DIRECTORY_WIN, student_email),
                error='Can\'t find output directory for {}'.format(student_email),
                run=run)

    # Check if we can find the results directory for the student.
    _check_path(student_email=student_email,
                path=join(OUTPUT_DIRECTORY_WIN, student_email, 'results.json'),
                error='Can\'t find results.json for {}'.format(student_email),
                run=run)

    # Send status to websocket.
    _send_message(student_email, 'Running', ':: Processing results..')

    # Load the json from the primary results.json file.
    with open(join(OUTPUT_DIRECTORY_WIN, student_email, 'results.json')) as f:
        data = json.loads(f.read())

    for t in data['tests']:
        # Our Test model instances are populated automatically from running tests
        # so new tests are automatically from the first time they are run.
        test, is_new = Test.objects.get_or_create(test=t['test'],
                                                  case=t['case'])

        # If the test didn't pass, we need to grab the log.
        passed = t['passed']
        log = ''

        if not passed:
            # Build an error message if reqd.
            message = 'Can\'t find error output for {} test for {}'
            message = message.format(str(test), student_email)

            error_file = t['error']
            path = join(OUTPUT_DIRECTORY_WIN, student_email, error_file)
            # Check that the error file exists.
            _check_path(student_email=student_email,
                        path=path, error=message, run=run)

            # Read the contents of the error file.
            with open(path) as f:
                log = f.read()

        detail = TestRunDetail(record=run, test=test, passed=passed, log=log)
        detail.save()

    # Send status to websocket.
    _send_message(student_email, 'Complete', 'Finished testing.')

    # Update the version number.
    run.test_version = data['version']
    run.status = 'Complete'
    run.save()


def _check_path(student_email, path, error, run):
    # Check if we can find the results directory for the student.
    if not exists(path):
        _send_message(student_email, 'Failed', ':: {}'.format(error))
        run.log += '\n{}\n'.format(error)
        run.status = 'Failed'
        run.save()
        raise NucleusException(error)


def _send_message(student_email, status, message):
    # We can only send a dict with text, accept, close and bytes
    # so we dump some json to a string and send it in the text
    # field.
    if not message.endswith('\n'):
        message += '\n'

    data = {
        'status': status,
        'message': message
    }
    Group(slugify(student_email)).send({'text': json.dumps(data)})


channel_routing = [
    route('run-tests', run_tests),
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect)
]
