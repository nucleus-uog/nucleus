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
from .models import User, TestRun, TestRunDetail
from .forms import UserForm
from django.db.models import Count

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


@user_passes_test(lambda u: u.is_staff)
def all_students(request):
    context_dict={'students': []}

    student_list = User.objects.all().order_by("last_name")
    for student in student_list:
        if not student.is_staff and student.is_active:
            context_dict['students'].append( {'guid': student.guid, 'name': student.get_full_name} )

    return render(request, 'nucleus/students.html', context=context_dict)


@login_required
def student(request, student_guid):
    context_dict={'tests': []}

    student = User.objects.get(email=student_guid+"@student.gla.ac.uk")
    context_dict['student'] = {'guid': student_guid, 'name': student.get_full_name}
    test_runs = TestRun.objects.filter(student=student).order_by('-date_run')

    for test_run in test_runs:

        #test_details = TestRunDetail.objects.filter(
                #record=test_run).annotate(max_score=Count('passed'))
                # .filter(
                # passed=True).annotate(score=Count('passed'))

        context_dict['tests'].append({
            'date': test_run.date_run,
            'version': test_run.test_version,
            'time': test_run.time_taken,
            'url': test_run.repository_url,
            #'score': test_details.score,
            #'max_score': test_details.max_score
         })

    return render(request, 'nucleus/student.html', context=context_dict)


@login_required
def demo(request):
    return render(request, 'nucleus/demo.html', context={})


@login_required
def demo_run(request):
    run = TestRun(student=request.user,
                  repository_url='https://github.com/davidtwco/uog-wad2.git')
    run.save()

    Channel('run-tests').send({'id': run.id})
    return JsonResponse({'status': 'Started..', 'message': 'Started..'})
