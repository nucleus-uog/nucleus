from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Student


# add @login_required
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
