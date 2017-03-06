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
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from rango import views

urlpatterns = [
    url(r'^$', views.sign_in, name='index'),
    url(r'^students/', views.all_students, name="all_students"),
	url(r'^sign-in/',views.sign_in, name="sign_in"),
	url(r'^register/',views.register, name="register"),
	url(r'^forgot-password',views.forgot_password, name="forgot_password"),
	url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^admin/', admin.site.urls),
]
