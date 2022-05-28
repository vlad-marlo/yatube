from django.contrib import admin
from django.urls import path
from django.urls.conf import include


urlpatterns = [
    path('', include('posts.urls', namespace='posts')),
    path('admin/', admin.site.urls),
    path('about/', include('about.urls', namespace='about')),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
]
