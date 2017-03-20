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


@login_required
def index(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('all_students'))
    return HttpResponseRedirect(reverse('student', kwargs={"student_guid":request.user.guid()}))


def register(request):
    if request.method =='POST':
        form = UserForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserForm()

    return render(request, 'nucleus/register.html', {'form': form})


@login_required
def account(request):
    if request.method == "POST":
        form = RepoForm(request.POST)
        if form.is_valid():
            userToUpdate = User.objects.get(email=form.cleaned_data['student_email'])
            userToUpdate.repository_url = form.cleaned_data['repository_url']
            userToUpdate.save()
        return HttpResponseRedirect(reverse('account'))
    else:
        form = RepoForm()

    context_dict = {'email': request.user.email,
                    'repository_url': request.user.repository_url,
                    'form': form}
    return render(request, 'nucleus/account.html', context_dict)


@user_passes_test(lambda u: u.is_staff)
def all_students(request):
    context_dict={'students': []}

    student_list = User.objects.all().order_by("last_name")
    totalScore = 0
    for student in student_list:
        if not student.is_staff and student.is_active and student.guid():
            try:
                test_run = TestRun.objects.filter(student=student).order_by('-date_run')[0]
                test_details = TestRunDetail.objects.filter(record=test_run)
                max_score = test_details.count()
                score = test_details.filter(passed=True).count()

                context_dict['students'].append({
                        'guid': student.guid,
                        'name': student.get_full_name,
                        'max_score': max_score,
                        'score': score,
                        'status': test_run.status,
                        'runid': test_run.id
                    })
                if test_run.status == 'Complete':
                    totalScore += score
            except:
                context_dict['students'].append({
                        'guid': student.guid,
                        'name': student.get_full_name,
                        'max_score': -1,
                        'score': -1,
                        'status': 'Complete',
                    })

    if len(context_dict['students']) == 0:
        context_dict['average'] = 0
    else:
        context_dict["average"] = totalScore / len(context_dict['students'])
    context_dict["totalTests"] = Test.objects.all().count()

    return render(request, 'nucleus/students.html', context=context_dict)


@login_required
def student(request, student_guid):
    if request.method == "POST":
        form = RepoForm(request.POST)
        if form.is_valid():
            userToUpdate = User.objects.get(email=form.cleaned_data['student_email'])
            userToUpdate.repository_url = form.cleaned_data['repository_url']
            userToUpdate.save()

            run = TestRun(student=userToUpdate,
                          repository_url=userToUpdate.repository_url)
            run.save()
            Channel('run-tests').send({'id': run.id})
        return HttpResponseRedirect(reverse('student', kwargs={"student_guid": student_guid}))

    form = RepoForm()
    student = User.objects.get(email=student_guid+"@student.gla.ac.uk")
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

    test_runs = TestRun.objects.filter(student=student).order_by('-date_run')
    for test_run in test_runs:

        test_details = TestRunDetail.objects.filter(record=test_run)

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
def testlog(request, student_guid, runid):
    student = User.objects.get(email=student_guid + "@student.gla.ac.uk")
    test_run = TestRun.objects.get(student=student, id=runid)
    test_details = TestRunDetail.objects.filter(record=test_run)

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
def specificTest(request, student_guid,runid,testid):

    student = User.objects.get(email=student_guid + "@student.gla.ac.uk")
    test_run = TestRun.objects.get(student=student, id=runid)

    test_details = TestRunDetail.objects.get(record=test_run, id=testid)
    if test_details.passed == True:
        passed = "Pass"
    else:
        passed = "Fail"

    if test_details.test.name:
        name = test_details.test.name
    else:
        name = test_details.test.test

    context_dict = {'name': name,
                    'description': test_details.test.description,
                    'group': test_details.test.category,
                    'passed': passed,
                    'log': test_details.log,
                    'guid': student_guid,
                    'runid': runid}

    return render(request, 'nucleus/test-feedback.html', context_dict)

@login_required
def check_status(request, runid):
    status = TestRun.objects.get(id=runid).status
    statusClasses = {
        'Error': 'badge-danger',
        'Pending': 'badge-warning',
        'Running': 'badge-warning',
        'Complete': 'badge-primary',
        'Failed': 'badge-danger'
    }
    className = "badge badge-pill mt-1 " + statusClasses[status]
    if status != "Complete" and status != "Error":
        className += " status-check"
    return JsonResponse({'status': status, 'id': runid, 'class': className})


@user_passes_test(lambda u: u.is_staff)
def run_all(request):
    students = User.objects.all().filter(is_staff=False, is_active=True)
    for student in students:
        if student.repository_url != "":
            run = TestRun(student=student,
                          repository_url=student.repository_url)
            run.save()
            Channel('run-tests').send({'id': run.id})

    return HttpResponseRedirect(reverse('all_students'))


@login_required
def demo(request):
    return render(request, 'nucleus/demo.html', context={})


#@login_required
def demo_run(request):
    run = TestRun(student=request.user,
                  repository_url='https://github.com/davidtwco/uog-wad2.git')
    run.save()

    Channel('run-tests').send({'id': run.id})
    return JsonResponse({'status': 'Started..', 'message': 'Started..'})
