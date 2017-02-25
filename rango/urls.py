from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'students/$', views.all_students, name='all_students'),
]
