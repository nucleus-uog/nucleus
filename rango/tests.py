from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib import auth
from .models import *
from .forms import *


class RegisterUserFormTest(TestCase):
   
    def test_UserForm_valid(self):
        """Checks that data must be entered into the form fields """

        form = UserForm(data={
            'first_name': 'John',
            'last_name': 'Devine',
            'email': '2162978D@student.gla.ac.uk',
            'password': 'Blueisthecolour',
            'confirm': 'Blueisthecolour'
        })

        self.assertTrue(form.is_valid())

#     def test_UserForm_invalid(self):
#         form = UserForm(data={
#             'first_name': '',
#             'last_name': 'Devine',
#             'email': '2162978D@gmail.com',
#             'password': 'Blueisthecolour',
#             'confirmPW': 'Blueisthe'
#         })
#         self.assertFalse(form.is_valid())
#
    def test_user_registration_success(self):
        """Checks that a user has been successfully registered"""

        response = self.client.post(reverse('register'), data={'first_name': 'John',
                                                         'last_name': 'Devine',
                                                         'email': '2162978D@student.gla.ac.uk',
                                                         'password': 'correctpassword',
                                                         'confirm': 'correctpassword'}, follow=True)

        user = User.objects.get(email='2162978D@student.gla.ac.uk')

        self.assertRedirects(response, reverse('student', kwargs={'student_guid': user.guid()}), status_code=302, target_status_code=200, msg_prefix="",
                             fetch_redirect_response=True)
        self.assertEqual('John Devine', user.get_full_name())


class LoginViewSuccessTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            first_name='John',
            last_name='Dev',
            email='2162978D@student.gla.ac.uk',
        )
        self.user.set_password('Blueisthecolour')
        self.user.save()

    def test_login_credentials_valid(self):
        """Checks that a valid user can login"""

        user_login = self.client.login(email='2162978D@student.gla.ac.uk', password='Blueisthecolour')
        self.assertTrue(user_login)
        user = auth.get_user(self.client)
        assert user.is_authenticated()
        response = self.client.get(reverse('student', kwargs={'student_guid': '2162978D'}))
        self.assertEqual(response.status_code, 200)

    def test_login_credentials_invalid(self):
        """Check that invalid user can't login"""

        response = self.client.post(reverse('sign_in'), {'username': 'wronguser', 'password': 'wrongpass'})

        # The sign is page should be reloaded.
        self.assertEqual(response.status_code, 200)
        # Check that error message is displayed.
        self.assertIn("Your username and password didn't match. Please try again.", response.content)

    def test_user_authenticated_login_success(self):
        """Check to make sure that a user who is already logged in can't do so again."""

        # Sign in user using given values.
        user_login = self.client.login(email='2162978D@student.gla.ac.uk', password='Blueisthecolour')
        self.assertTrue(user_login)
        user = auth.get_user(self.client)
        assert user.is_authenticated()

    def test_user_authenticated_login_failure(self):
        """Check to make sure that a user is not authenticated if login fails"""

        user_login = self.client.login(email='john@email.com', password='password')
        self.assertFalse(user_login)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())

    def tearDown(self):
        self.user.delete()


# class StatusCheckTest(TestCase):
#
#     def setUp(self):
#         self.test_run = TestRun.objects.create(
#             student='2162978D@student.gla.ac.uk',
#             repository_url= "https://www.github.com/james/project",
#             date_run="05/05/17",
#             tets_version='0.01a',
#             log='',
#             time_taken='0.003',
#             status='Error'
#         )
#
#         self.test_run.save()
#
#
#     def test_check_status_view_classes(self):
#
#         response = self.client.get(reverse('student', kwargs='2162978D'))
#         print response




















