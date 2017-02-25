from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# add @login_required
def all_students(request):
    response = render(request, 'nucleus/students.html', context={})
    return response


