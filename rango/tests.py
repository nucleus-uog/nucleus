from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import *
from .forms import *


class SetupClass(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            first_name='John',
            last_name='Dev',
            email='2162978D@student.gla.ac.uk',
            password='Blueisthecolour',
            confirmPW='Blueisthecolour')


class RegisterUserFormTest(TestCase):

    def test_UserForm_valid(self):
        '''Checks that data must be entered into the form fields '''
        form = UserForm(data={
            'first_name': 'John',
            'last_name': 'Devine',
            'email': '2162978D@student.gla.ac.uk',
            'password': 'Blueisthecolour',
            'confirmPW': 'Blueisthecolour'
        })
        self.assertTrue(form.is_valid())

    def test_UserForm_invalid(self):
        form = UserForm(data={
            'first_name': '',
            'last_name': 'Devine',
            'email': '2162978D@gmail.com',
            'password': 'Blueisthecolour',
            'confirmPW': 'Blueisthe'
        })
        self.assertFalse(form.is_valid())



