"""nucleus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^students/$', views.all_students, name="all_students"),
    url(r'^student/(?P<student_guid>[\w\-]+)/$', views.student, name='student'),
    # Auth
    url(r'^sign-in$',auth_views.login, {'template_name': 'nucleus/sign-in.html'}, name="sign_in"),
    url(r'^logout$', auth_views.logout, name='user_logout'),
    url(r'^register$',views.register, name="register"),
    url(r'^account$',views.account, name="account"),
    url(r'^forgot-password$',auth_views.password_change, name="forgot_password"),
    url(r'^forgot-password/done$',auth_views.password_change_done, name="forgot_password"),
    url(r'^password_reset$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^admin/', admin.site.urls),
    url(r'^demo/$', views.demo, name='demo'),
    url(r'^demo/run/$', views.demo_run, name='demo_run')
]
