from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^createuser$', views.createuser),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^dashboard/(?P<friend_id>\d+)/add$', views.poke),
    url(r'^logout$', views.logout)
]
