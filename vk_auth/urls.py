from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^auth/', views.auth, name='auth'),
    url(r'^get_token/', views.get_token, name='get_token'),
    url(r'^friends_list/$', views.get_friends_list, name='friends_list'),
]
