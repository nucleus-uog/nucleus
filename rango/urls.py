from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^students/$', views.all_students, name="all_students"),
    url(r'^student/(?P<student_guid>[\w\-]+)/$', views.student, name='student'),
    url(r'^demo/$', views.demo, name='demo'),
    url(r'^demo/run/$', views.demo_run, name='demo_run'),
    url(r'^register$', views.register, name="register"),
    url(r'^account$', views.account, name="account"),
]
