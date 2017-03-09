import time
import os
import shutil
import json
from os.path import join, exists

from datetime import timedelta
import docker
from django.template.defaultfilters import slugify
from channels import Group

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
        raise NucleusException('Test Run instance not found.')

    if run.status == 'Complete':
        raise NucleusException('Started TestRun for a instance '
                               'that is already complete.')

    # Get details.
    student_email = run.student.email
    repository_url = run.repository_url

    # Log the start time.
    start = time.time()

    # Set up our environment variables and 
    # volumes for running the container.
    environment = {
        'TESTS_STUDENT': student_email,
        'TESTS_REPO_URL': repository_url
    }

    # Remove previous results
    student_directory = join(OUTPUT_DIRECTORY_WIN, student_email)
    if exists(student_directory):
        shutil.rmtree(student_directory)

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
        Group(slugify(student_email)).send({
            'status': 'Running',
            'next_line': line
        })

    # Get the end time.
    end = time.time()

    # Update the details of the run instance
    # with the details from the container.
    run.log = container.logs()
    run.status = 'Running'
    run.test_version = 'N/A'
    run.time_taken = timedelta(seconds=end-start)
    run.save()

    _collect_results(student_email, run)


def _collect_results(student_email, run):
    # Check if we can find the results directory for the student.
    _check_path(path=join(OUTPUT_DIRECTORY_WIN, student_email),
                error='Can\'t find output directory for {}'.format(student_email),
                run=run)

    # Check if we can find the results directory for the student.
    _check_path(path=join(OUTPUT_DIRECTORY_WIN, student_email, 'results.json'),
                error='Can\'t find results.json for {}'.format(student_email),
                run=run)

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
            _check_path(path=path, error=message, run=run)

            # Read the contents of the error file.
            with open(path) as f:
                log = f.read()

        detail = TestRunDetail(record=run, test=test, passed=passed, log=log)
        detail.save()

    # Update the version number.
    run.test_version = data['version']
    run.status = 'Complete'
    run.save()


def _check_path(path, error, run):
    # Check if we can find the results directory for the student.
    if not exists(path):
        run.log += '\n{}\n'.format(error)
        run.status = 'Failed'
        run.save()
        raise NucleusException(error)