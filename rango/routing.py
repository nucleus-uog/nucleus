from channels.routing import route
from .tasks import run_tests

channel_routing = [
    route('run-tests', run_tests)
]