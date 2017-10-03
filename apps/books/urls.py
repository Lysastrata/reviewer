from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^books$', views.home),
    url(r'^books/add$', views.review),
    url(r'^books/(?P<book_id>\d+)$', views.book),
    url(r'^books/(?P<user_id>\d+)$', views.user),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
]
