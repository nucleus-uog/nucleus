from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^students/$', views.all_students, name="all_students"),
    url(r'^student/(?P<student_guid>\d{7}[A-Za-z])/$', views.student, name='student'),
    url(r'^student/(?P<student_guid>[\w\-]+)/run/$', views.testlog, name='testlog' ),
    url(r'^student/(?P<student_guid>[\w\-]+)/run/[\w\-]+/test/run/[\w\-]+$', views.specificTest, name='specificTest' ),
    url(r'^status/(?P<runid>\d+)/$', views.check_status, name='check_status'),
    url(r'^demo/$', views.demo, name='demo'),
    url(r'^demo/run/$', views.demo_run, name='demo_run'),
    url(r'^run_all/$', views.run_all, name="run_all"),
    url(r'^register$', views.register, name="register"),
    url(r'^account$', views.account, name="account"),
]
