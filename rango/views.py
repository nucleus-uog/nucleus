from channels import Channel
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
    JsonResponse
)
from django.contrib.auth.decorators import user_passes_test
from .models import (
    User,
    Test,
    TestRun,
    TestRunDetail
)
from .forms import UserForm
from django.db.models import Count
from django.views.generic.edit import UpdateView


@login_required
def index(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('all_students'))
    return HttpResponseRedirect(reverse('student', kwargs={"student_guid":request.user.guid()}))

def register(request):
    registered = False
    if request.method =='POST':
        user_form=UserForm(data=request.POST)
        if user_form.is_valid() and user_form.cleaned_data['password'] == user_form.cleaned_data['confirmPW']:
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            registered=True
        elif user_form.data['password'] != user_form.data['confirmPW']:
            user_form.add_error('confirmPW', 'The passwords do not match')
        else:
            print(user_form.errors)
    else:
        user_form=UserForm()

    return render(request, 'nucleus/register.html',{'user_form':user_form, 'registered':registered})


@login_required
def account(request):
    if request.method == "POST":
        userToUpdate = User.objects.get(email=request.user.email)
        userToUpdate.repository_url = request.POST.get("newRepo", "")
        userToUpdate.save()
    context_dict = {'email': request.user.email, 'repository_url': request.user.repository_url}
    return render(request, 'nucleus/account.html', context_dict)


@user_passes_test(lambda u: u.is_staff)
def all_students(request):
    context_dict={'students': []}

    student_list = User.objects.all().order_by("last_name")
    totalScore = 0
    for student in student_list:
        if not student.is_staff and student.is_active:

            try:
                test_run = TestRun.objects.filter(student=student).order_by('-date_run')[0]
                test_details = TestRunDetail.objects.filter(record=test_run)
                max_score = test_details.count()
                score = test_details.filter(passed=True).count()
            except:
                max_score = -1
                score = -1

            context_dict['students'].append({
                    'guid': student.guid,
                    'name': student.get_full_name,
                    'max_score': max_score,
                    'score': score,
                    'status': test_run.status
                })
            if test_run.status == 'Complete':
                totalScore += score

    context_dict["average"] = totalScore/ len(context_dict['students'])
    context_dict["totalTests"] = Test.objects.all().count()

    return render(request, 'nucleus/students.html', context=context_dict)


@login_required
def student(request, student_guid):
    context_dict={'tests': []}

    student = User.objects.get(email=student_guid+"@student.gla.ac.uk")
    context_dict['student'] = {'guid': student_guid, 'name': student.get_full_name, 'repository_url': student.repository_url}
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
            'max_score': test_details.count()
         })

    return render(request, 'nucleus/student.html', context=context_dict)


@login_required
def demo(request):
    return render(request, 'nucleus/demo.html', context={})


@login_required
def demo_run(request):
    run = TestRun(student=request.user,
                  repository_url=request.user.repository_url)
    run.save()

    Channel('run-tests').send({'id': run.id})
    return JsonResponse({'status': 'Started..', 'message': 'Started..'})
