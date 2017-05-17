"""myblog URL Configuration

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
from django.conf.urls import url ,include
from django.contrib import admin

from blog.sitemaps import PostSitemap
from django.contrib.sitemaps.views import sitemap

from myblog.settings import DEBUG

sitemaps={
    'posts': PostSitemap,
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls',namespace='blog')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps':sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^users/', include('users.urls', namespace='users')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]


#for django-debug-toolbar  static file
if DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))