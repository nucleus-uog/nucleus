from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib import auth
from .models import *
from .forms import *
import json

class RegisterUserFormTest(TestCase):
    """Checks that data must be entered into the form fields """

    def test_UserForm_valid(self):
        form = UserForm(data={
            'first_name': 'John',
            'last_name': 'Devine',
            'email': '2162978D@student.gla.ac.uk',
            'password': 'Blueisthecolour',
            'confirm': 'Blueisthecolour'
        })

        self.assertTrue(form.is_valid())

    def test_UserForm_different_passwords(self):
        form = UserForm(data={
            'first_name': 'John',
            'last_name': 'Devine',
            'email': '2162978D@student.gla.ac.uk',
            'password': 'Blueisthecolour',
            'confirm': 'Blueisthe'
        })
        self.assertFalse(form.is_valid())

    def test_UserForm_wrong_email_suffix(self):
        form = UserForm(data={
            'first_name': 'John',
            'last_name': 'Devine',
            'email': '2162978D@gmail.com',
            'password': 'Blueisthecolour',
            'confirm': 'Blueisthecolour'
        })
        self.assertFalse(form.is_valid())

    def test_UserForm_wrong_email_prefix(self):
        form = UserForm(data={
            'first_name': 'John',
            'last_name': 'Devine',
            'email': 'johndevine@student.gla.ac.uk',
            'password': 'Blueisthecolour',
            'confirm': 'Blueisthecolour'
        })
        self.assertFalse(form.is_valid())

    def test_user_registration_success(self):
        """Checks that a user has been successfully registered"""

        response = self.client.post(reverse('register'), data={'first_name': 'John',
                                                               'last_name': 'Devine',
                                                               'email': '2162978D@student.gla.ac.uk',
                                                               'password': 'correctpassword',
                                                               'confirm': 'correctpassword'}, follow=True)

        user = User.objects.get(email='2162978D@student.gla.ac.uk')

        self.assertRedirects(response, reverse('student', kwargs={'student_guid': user.guid()}), status_code=302,
                             target_status_code=200, msg_prefix="",
                             fetch_redirect_response=True)
        self.assertEqual('John Devine', user.get_full_name())


class LoginViewTest(TestCase):
    """Test different scenarios that the login """

    def setUp(self):
        self.user = User.objects.create(
            first_name='John',
            last_name='Dev',
            email='2162978D@student.gla.ac.uk',
        )
        self.user.set_password('Blueisthecolour')
        self.user.save()

    def test_login_credentials_invalid(self):
        """Check that invalid user can't login"""

        response = self.client.post(reverse('sign_in'), {'username': 'wronguser', 'password': 'wrongpass'})

        # The sign is page should be reloaded.
        self.assertEqual(response.status_code, 200)
        # Check that error message is displayed.
        self.assertIn("Your username and password didn't match. Please try again.", response.content)

    def test_user_authenticated_login_success(self):
        """Check to make sure that a user who has logged in, is authenticated."""

        # Sign in user using given values.
        self.client.post(reverse('sign_in'), data={
            'username': self.user.email,
            'password': 'Blueisthecolour'
        }, follow=True)

        self.assertTrue(self.user.is_authenticated())

    def test_user_authenticated_login_failure(self):
        """Check to make sure that a user is not authenticated if login fails"""

        user_login = self.client.login(email='john@email.com', password='password')
        self.assertFalse(user_login)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())

    def tearDown(self):
        self.user.delete()


class StatusCheckTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='2162978D@student.gla.ac.uk',
            password='Greenisthecolour',
            first_name='John',
            last_name='Devine',
            repository_url='https://github.com/batman',
        )

        self.user.set_password('Greenisthecolour')
        self.user.save()
        self.test_run1 = TestRun.objects.create(
            student=self.user,
            status='Error'
        )
        self.test_run1.save()

        self.test_run2 = TestRun.objects.create(
            student=self.user,
            status='Pending'
        )
        self.test_run2.save()

        self.test_run3 = TestRun.objects.create(
            student=self.user,
            status='Running'
        )
        self.test_run3.save()

        self.test_run4 = TestRun.objects.create(
            student=self.user,
            status='Complete'
        )
        self.test_run4.save()

        self.test_run5 = TestRun.objects.create(
            student=self.user,
            status='Failed'
        )
        self.test_run5.save()

        self.client.login(email='2162978D@student.gla.ac.uk', password='Greenisthecolour')

    def test_check_status_prror_class(self):
        response = self.client.get((reverse('check_status', kwargs={'runid': self.test_run1.id})), follow=True)
        content = json.loads(response.content)

        self.assertEqual(content['status'], 'Error')
        self.assertEqual(content['id'], str(self.test_run1.id))
        self.assertEqual(content['class'], 'badge badge-pill mt-1 badge-danger')
        self.assertEqual(content['icon'], 'fa fa-exclamation-triangle')

    def test_check_status_pending_class(self):
        response = self.client.get((reverse('check_status', kwargs={'runid': self.test_run2.id})), follow=True)
        content = json.loads(response.content)

        self.assertEqual(content['status'], 'Pending')
        self.assertEqual(content['id'], str(self.test_run2.id))
        self.assertEqual(content['class'], 'badge badge-pill mt-1 badge-warning status-check')
        self.assertEqual(content['icon'], 'fa fa-circle-o-notch fa-spin fa-fw')

    def test_check_status_running_class(self):
        response = self.client.get((reverse('check_status', kwargs={'runid': self.test_run3.id})), follow=True)
        content = json.loads(response.content)

        self.assertEqual(content['status'], 'Running')
        self.assertEqual(content['id'], str(self.test_run3.id))
        self.assertEqual(content['class'], 'badge badge-pill mt-1 badge-warning status-check')
        self.assertEqual(content['icon'], 'fa fa-circle-o-notch fa-spin fa-fw')

    def test_check_status_complete_class(self):
        response = self.client.get((reverse('check_status', kwargs={'runid': self.test_run4.id})), follow=True)
        content = json.loads(response.content)

        self.assertEqual(content['status'], 'Complete')
        self.assertEqual(content['id'], str(self.test_run4.id))
        self.assertEqual(content['class'], 'badge badge-pill mt-1 badge-primary')
        self.assertEqual(content['icon'], 'fa fa-check')






class IndexViewTest(TestCase):
    """Checks what page a valid user goes to depending on if they have staff status"""

    def setUp(self):
        self.admin = User.objects.create(
            email='jerry.seinfeld@email.com',
            password='George',
            is_staff=True,
            is_active=True
        )
        self.admin.set_password('George')
        self.admin.save()

        self.student = User.objects.create(
            email='2162978D@student.gla.ac.uk',
            password='Blueisthecolour',
            first_name='Steve',
            last_name='Jobs',
            is_staff=False,
            is_active=True,
        )
        self.student.set_password('Blueisthecolour')
        self.student.save()

    def test_login_staff_redirect(self):
        """Checks that when a staff user signs in that it redirects them to the correct page."""
        response = self.client.post(reverse('sign_in'), data={
            'username': self.admin.email,
            'password': 'George'
        }, follow=True)

        self.assertRedirects(response, reverse('all_students'), status_code=302,
                             target_status_code=200, msg_prefix="",
                             fetch_redirect_response=True)
        self.assertIn('Steve Jobs (2162978D)', response.content)

    def test_login_student_redirect(self):
        """Checks that when a student user signs in that it redirects them to the correct page."""
        response = self.client.post(reverse('sign_in'), data={
            'username': self.student.email,
            'password': 'Blueisthecolour'
        }, follow=True)

        self.assertRedirects(response, reverse('student', kwargs={'student_guid': '2162978D'}),
                             status_code=302, target_status_code=200, msg_prefix="",
                             fetch_redirect_response=True)

        self.assertIn('No tests have been ran for this student.', response.content)





