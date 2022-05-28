from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', view=views.index, name='index'),
    path('group/<slug:slug>', view=views.group_list, name='group_list'),
]
