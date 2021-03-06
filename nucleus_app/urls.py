from django.conf.urls import url
from . import views

# Add the url patterns used in the application itself.
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^students/$', views.all_students, name="all_students"),
    url(r'^student/(?P<student_guid>\d{7}[A-Za-z])/$', views.student, name='student'),
    url(r'^student/(?P<student_guid>[\w\-]+)/run/(?P<runid>\d+)/$', views.testlog, name='testlog' ),
    url(r'^student/(?P<student_guid>[\w\-]+)/run/(?P<runid>\d+)/test/(?P<testid>\d+)/$', views.specificTest, name='specificTest' ),
    url(r'^status/(?P<runid>\d+)/$', views.check_status, name='check_status'),
    url(r'^run_all/$', views.run_all, name="run_all"),
    url(r'^register$', views.register, name="register"),
    url(r'^account$', views.account, name="account"),
]
