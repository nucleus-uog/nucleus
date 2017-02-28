from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Student
from rango.forms import UserForm
from django.http import HttpResponseRedirect, HttpResponse 
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test


def staff(user):

	stafflist=['1']		#List of all staff users allowed to access all students details
	if (user.username in stafflist):
		return True
	
@user_passes_test(staff)
def all_students(request):

    #student_list = Student.objects.order_by('guid')

    context_dict = { 'students': [
                        {'guid': '2198970T', 'name': 'Charlie Thomas', 'score': 69},
                        {'guid': '2198989S', 'name': 'John Smith', 'score': 34},
                        {'guid': '2174939D', 'name': 'Jared Dunn', 'score': 50},
                        {'guid': '2598741W', 'name': 'William Wonka', 'score': 69},
                        {'guid': '2174057L', 'name': 'James Lorne', 'score': 11},
                        {'guid': '2134567R', 'name': 'Ewan Redface', 'score': 43},
                        {'guid': '2198970T', 'name': 'Charlie Thomas', 'score': 69},
                        {'guid': '2198989S', 'name': 'John Smith', 'score': 34},
                        {'guid': '2174939D', 'name': 'Jared Dunn', 'score': 50},
                        {'guid': '2598741W', 'name': 'William Wonka', 'score': 69},
                        {'guid': '2174057L', 'name': 'James Lorne', 'score': 11},
                        {'guid': '2134567R', 'name': 'Ewan Redface', 'score': 43},
                        {'guid': '2198970T', 'name': 'Charlie Thomas', 'score': 69},
                        {'guid': '2198989S', 'name': 'John Smith', 'score': 34},
                        {'guid': '2174939D', 'name': 'Jared Dunn', 'score': 50},
                        {'guid': '2598741W', 'name': 'William Wonka', 'score': 69},
                        {'guid': '2174057L', 'name': 'James Lorne', 'score': 11},
                        {'guid': '2134567R', 'name': 'Ewan Redface', 'score': 43}]
                    }

    return render(request, 'nucleus/students.html', context=context_dict)


	
def register(request):
	registered = False
	if request.method =='POST':
		user_form=UserForm(data=request.POST)
		if user_form.is_valid()and user_form.cleaned_data['password']==user_form.cleaned_data['confirmPW']:
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

#todo
def forgot_password(request):
	return render(request, 'nucleus/sign-in.html')
	
def sign_in(request): 	
	if request.method == 'POST':
		username = request.POST.get('username') 
		password = request.POST.get('password')
		
		user = authenticate(username=username, password=password)
		if user: 
			if user.is_active:
				login(request, user) 
				return HttpResponseRedirect(reverse('all_students')) 
			else: 
				return HttpResponse("Your account is disabled.") 
		else:
			print("Invalid login details: {0}, {1}".format(username, password)) 
			invalid = 'Invalid login details supplied.'
			return render(request, 'nucleus/sign-in.html', {'invalid':invalid})
	else:
		return render(request, 'nucleus/sign-in.html', {})

@login_required		
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('sign_in'))