"""taoxuezhe_project URL Configuration

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
from django.conf.urls import include ##首先要引用include，然后才能借用其他的URLconf
from django.conf import settings
from django.views.static import serve ##这是django1.10的一个改动

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^predict/',include('predict.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),#the doc for registration：https://docs.djangoproject.com/en/1.9/topics/auth/default/#django.contrib.auth.views.password_change


]
if settings.DEBUG:  ##为了配置media server
    urlpatterns +=[
        url(r'^media/(?P<path>.*)$',serve,{
            'document_root':settings.MEDIA_ROOT,
        },)]