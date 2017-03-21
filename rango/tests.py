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
        )
        self.user.set_password('Blueisthecolour')
        self.user.save()






class RegisterUserFormTest(TestCase):
    '''Checks that data must be entered into the form fields '''
    def test_UserForm_valid(self):
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

class LoginViewSuccessTest(TestCase):

    '''Checks that a valid user can login'''
    def test_login_credentials_valid(self):

        self.user = User.objects.create(
            first_name='John',
            last_name='Dev',
            email='2162978D@student.gla.ac.uk',
        )

        self.user.set_password('Blueisthecolour')
        self.user.save()
        user = User.objects.get(email='2162978D@student.gla.ac.uk')
        user_login = self.client.login(email='2162978D@student.gla.ac.uk', password='Blueisthecolour')
        self.assertTrue(user_login)
        response = self.client.get(reverse('student', kwargs={'student_guid':'2162978D'}))
        self.assertEqual(response.status_code,200)

    #Check that invalid user can't login 







