import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nucleus.settings")

import django
django.setup()

# Load dummy data from fixtures 
from django.core.management import call_command
call_command('loaddata', "complete_students.json", verbosity=0)
