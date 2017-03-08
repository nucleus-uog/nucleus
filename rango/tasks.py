import logging
import time
import os
from channels import Group
import docker
from .models import TestRun


IMAGE_URL = 'registry.gitlab.com/devine-industries/nucleus-tests:master'
VOLUMES = {
    './results/': {
        'bind': '/nucleus/results',
        'mode': 'rw'
    }
}


logger = logging.getLogger('runner')
client = docker.from_env()
client.login(registry='registry.gitlab.com',
             username=os.environ['NUCLEUS_REGISTRY_USERNAME'],
             password=os.environ['NUCLEUS_REGISTRY_PASSWORD'])


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
        logger.error('Test Run instance not found.')
        return

    if run.status == 'Complete':
        logger.error('Started TestRun for a instance '
                     'that is already complete.')
        return

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
    container = client.containers.run(IMAGE_URL, environment=environment,
                                      volumes=VOLUMES, detach=True)
    
    # As the logs come in, stream them back to the 
    # listening websocket, if it exists.
    for line in container.logs(stream=True):
        Group(student_email).send({
            'status': 'Running',
            'next_line': line
        })

    # Get the end time.
    end = time.time()

    # Update the details of the run instance
    # with the details from the container.
    run.log = container.logs()
    run.status = 'Finished'
    run.time_taken = end - start

    # Save the instance.
    run.save()

