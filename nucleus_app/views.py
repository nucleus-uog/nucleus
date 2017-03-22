from channels import Channel
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test
)
from django.db.models import Count
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
    JsonResponse
)
from .models import (
    User,
    Test,
    TestRun,
    TestRunDetail
)
from .forms import UserForm, RepoForm
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from .decorators import correct_student


@login_required
def index(request):
    """
    Checks if the user is staff, if so we take them to the all students page, else their tests
    page.
    """
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('all_students'))
    return HttpResponseRedirect(reverse('student', kwargs={"student_guid":request.user.guid()}))


def register(request):
    """Registers the user and logs them in."""
    if request.method =='POST':
        # Validate our register form using the UserForm.
        form = UserForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            # Login with our new user and redirect to index.
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserForm()

    return render(request, 'nucleus/register.html', {'form': form})


@login_required
def account(request):
    # Check if we are posting a repository url change.
    if request.method == "POST":
        form = RepoForm(request.POST)
        if form.is_valid():
            # Get the student email and the repository url from the form and
            # save them to the user.
            userToUpdate = User.objects.get(email=form.cleaned_data['student_email'])
            userToUpdate.repository_url = form.cleaned_data['repository_url']
            userToUpdate.save()
        return HttpResponseRedirect(reverse('account'))
    else:
        form = RepoForm()

    # Get our context for the account page.
    context_dict = {
        'fullname': request.user.get_full_name(),
        'email': request.user.email,
        'repository_url': request.user.repository_url,
        'form': form
    }
    return render(request, 'nucleus/account.html', context_dict)


# We ensure that the user is staff to view the all students page.
@user_passes_test(lambda u: u.is_staff)
def all_students(request):
    context_dict={'students': []}

    # Get all the students ordered by last name.
    student_list = User.objects.all().order_by("last_name")
    totalScore = 0
    for student in student_list:
        # Check the student isn't staff, is active and that their email has a guid.
        if not student.is_staff and student.is_active and student.guid():
            try:
                # Get the most recent test run from each user.
                test_run = TestRun.objects.filter(student=student).order_by('-date_run')[0]
                # Get the detail rows for the given test run.
                test_details = TestRunDetail.objects.filter(record=test_run)
                # Find out how many tests were run against this user.
                max_score = test_details.count()
                # Find out many of those tests actually passed.
                score = test_details.filter(passed=True).count()

                # Append the context for each student to the list.
                context_dict['students'].append({
                    'guid': student.guid,
                    'name': student.get_full_name,
                    'max_score': max_score,
                    'score': score,
                    'status': test_run.status,
                    'runid': test_run.id
                })

                # If the test run finished, add their score to the running total.
                if test_run.status == 'Complete':
                    totalScore += score
            except:
                # If we can't find a test run, add enough detail to show
                # a row on the page.
                context_dict['students'].append({
                        'guid': student.guid,
                        'name': student.get_full_name,
                        'max_score': -1,
                        'score': -1,
                        'status': 'Complete',
                    })

    # Check if we have any students before calculating the average to avoid division by zero.
    if len(context_dict['students']) == 0:
        context_dict['average'] = 0
    else:
        context_dict["average"] = totalScore / len(context_dict['students'])
    # Add the total number of tests to the context for the statistics.
    context_dict["totalTests"] = Test.objects.all().count()

    return render(request, 'nucleus/students.html', context=context_dict)


@login_required
@correct_student
def student(request, student_guid):
    # If we are submitting a repository url change (by pressing 'run tests').
    if request.method == "POST":
        form = RepoForm(request.POST)
        if form.is_valid():
            # Update the user with the submitted url, in case it has changed.
            userToUpdate = User.objects.get(email=form.cleaned_data['student_email'])
            userToUpdate.repository_url = form.cleaned_data['repository_url']
            userToUpdate.save()

            # Queue up a test run.
            run = TestRun(student=userToUpdate,
                          repository_url=userToUpdate.repository_url)
            run.save()
            Channel('run-tests').send({'id': run.id})
        return HttpResponseRedirect(reverse('student', kwargs={"student_guid": student_guid}))

    form = RepoForm()
    # Find the student for the current guid.
    student = User.objects.get(email=student_guid+"@student.gla.ac.uk")
    # Build a context dict with information required by the page.
    context_dict={
        'tests': [],
        'form': form,
        'student': {
            'guid': student_guid,
            'email': student.email,
            'name': student.get_full_name,
            'repository_url': student.repository_url
        }
    }

    # Find the test runs for the given user, sorted by most recent.
    test_runs = TestRun.objects.filter(student=student).order_by('-date_run')
    for test_run in test_runs:
        # Get the details for that test run.
        test_details = TestRunDetail.objects.filter(record=test_run)

        # Build up our context with the information required to show the details..
        context_dict['tests'].append({
            'date': test_run.date_run,
            'version': test_run.test_version,
            'time': test_run.time_taken,
            'url': test_run.repository_url,
            'status': test_run.status,
            'score': test_details.filter(passed=True).count(),
            'max_score': test_details.count(),
            'id': test_run.id
         })

    return render(request, 'nucleus/student.html', context=context_dict)


@login_required
@correct_student
def testlog(request, student_guid, runid):
    # Find the current student and test run for given url parameters.
    student = User.objects.get(email=student_guid + "@student.gla.ac.uk")
    test_run = TestRun.objects.get(student=student, id=runid)
    # Find the test run details for the given run.
    test_details = TestRunDetail.objects.filter(record=test_run)

    # Build the basic context with the information we have.
    context_dict = {
        'test': {
            'version': test_run.test_version,
            'time': test_run.time_taken,
            'url': test_run.repository_url
        },
        'chapter_test': [],
        'logs': test_run.log,
        'runid': runid,
        'status': test_run.status,
        'date': test_run.date_run,
        'guid': student_guid
    }

    # Go through each test and add the details for it to the context.
    for chapter_test in test_details:
        if chapter_test.passed == True:
            passed = "Pass"
        else:
            passed = "Fail"

        if chapter_test.test.name:
            name = chapter_test.test.name
        else:
            name = chapter_test.test.test

        context_dict['chapter_test'].append({
            'name': name,
            'description': chapter_test.test.description,
            'group': chapter_test.test.category,
            'passed': passed,
            'testid': chapter_test.id
        })

    return render(request,'nucleus/test-run.html', context=context_dict)

@login_required
@correct_student
def specificTest(request, student_guid, runid, testid):
    # Get the student, test run and test detail for the given parameters.
    student = User.objects.get(email=student_guid + "@student.gla.ac.uk")
    test_run = TestRun.objects.get(student=student, id=runid)
    test_details = TestRunDetail.objects.get(record=test_run, id=testid)

    # Replace the True/False with Pass/Fail
    if test_details.passed == True:
        passed = "Pass"
    else:
        passed = "Fail"

    # Sets test to readable name if it exists
    if test_details.test.name:
        name = test_details.test.name
    else:
        name = test_details.test.test

    # Build our context.
    context_dict = {
        'name': name,
        'description': test_details.test.description,
        'group': test_details.test.category,
        'passed': passed,
        'log': test_details.log,
        'guid': student_guid,
        'runid': runid
    }

    return render(request, 'nucleus/test-feedback.html', context_dict)


@login_required
def check_status(request, runid):
    # Get the status of the test run we are querying.
    status = TestRun.objects.get(id=runid).status

    # Declare our mapping of badge colours to status'.
    statusClasses = {
        'Error': 'badge-danger',
        'Pending': 'badge-warning',
        'Running': 'badge-warning',
        'Complete': 'badge-primary',
        'Failed': 'badge-danger'
    }

    # Declare our mapping of badge icons to status'.
    iconClasses = {
        'Error': 'fa fa-exclamation-triangle',
        'Pending': 'fa fa-circle-o-notch fa-spin fa-fw',
        'Running': 'fa fa-circle-o-notch fa-spin fa-fw',
        'Complete': 'fa fa-check',
        'Failed': 'fa fa-exclamation-triangle'
    }

    # Build the class name based on the bootstrap classes and the given status.
    className = "badge badge-pill mt-1 " + statusClasses[status]
    if status != "Complete" and status != "Error":
        # If the status could change in future, add the class that triggers the ping.
        className += " status-check"

    # Return json to be parsed by our javascript.
    return JsonResponse({'status': status, 'id': runid, 'class': className, 'icon': iconClasses[status]})


@user_passes_test(lambda u: u.is_staff)
def run_all(request):
    # Get a list of all active students that aren't staff.
    students = User.objects.all().filter(is_staff=False, is_active=True)

    for student in students:
        # Check if the student has a repository url.
        if student.repository_url != "":

            # Check if a student currently has a test runnning
            recent_test_run = TestRun.objects.filter(student=student).order_by('-date_run')[0]
            if recent_test_run.status != "Running" and recent_test_run.status != "Pending":
                # Queue up a test run for the user.
                run = TestRun(student=student,
                              repository_url=student.repository_url)
                run.save()
                Channel('run-tests').send({'id': run.id})

    # Redirect back to all students.
    return HttpResponseRedirect(reverse('all_students'))
