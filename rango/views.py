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
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test
from .models import User, TestRun
from .forms import UserForm


@user_passes_test(lambda u: u.is_staff)
def all_students(request):
    context_dict={'students': []}

    student_list = User.objects.all().order_by("last_name")
    for student in student_list:
        if not student.is_staff and student.is_active:
            context_dict['students'].append( {'guid': student.guid, 'name': student.get_full_name} )

    return render(request, 'nucleus/students.html', context=context_dict)


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


def forgot_password(request):
    return render(request, 'nucleus/sign-in.html')


def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if (user.is_staff):	#if user is staff send them toall students page
                    return HttpResponseRedirect(reverse('all_students'))
                else:
                    return HttpResponseRedirect(reverse('student'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(email, password))
            invalid = 'Invalid login details supplied.'
            return render(request, 'nucleus/sign-in.html', {'invalid': invalid})
    else:
        return render(request, 'nucleus/sign-in.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('sign_in'))


@login_required
def student(request, student_guid):
    context_dict={'tests': []}

    student = User.objects.get(email=student_guid+"@student.gla.ac.uk")
    context_dict['student'] = {'guid': student_guid, 'name': student.get_full_name}
    test_runs = TestRun.objects.all().filter(student=student)

    for test_run in test_runs:
        context_dict['tests'].append( {'date': test_run.date_run,
                                       'version': test_run.version,
                                       'time': test_run.time_taken,
                                       'url': test_run.repository_url
                                       } )

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
