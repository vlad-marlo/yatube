from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', view=views.index, name='index'),
    path('group/<slug:slug>', view=views.group_list, name='group_list'),
    path('profile/<str:username>/', view=views.profile, name='profile'),
    path('posts/<int:post_id>/', view=views.post_detail, name='post_detail'),
    path('create', views.post_create, name='create'),
    path('posts/<int:post_id>/edit/', view=views.post_edit, name='post_edit'),
]
