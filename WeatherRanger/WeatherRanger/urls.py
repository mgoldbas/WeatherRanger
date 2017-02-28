"""WeatherRanger URL Configuration

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
from django.conf.urls import url, include
from django.http import HttpResponseRedirect
from WeatherRangerProject.views import EnterRangeView, CreateUserView, ListCityView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^weather/', include('WeatherRangerProject.urls', namespace = 'weather')),
    url(r'^$', login_required(EnterRangeView.as_view(), login_url='/login/'), name='home'),
    url(r'^create-user/$', CreateUserView.as_view(), name='create-user'),
    url(r'^cities/$', ListCityView.as_view(), name='cities'),

]

urlpatterns += [
    url('^', include('django.contrib.auth.urls', namespace='accounts')),
    url('^accounts/', include('django.contrib.auth.urls', namespace='accounts')),

]
