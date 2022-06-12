from django.urls import path, include
from rest_framework.authtoken import views as auth
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, GroupViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='comments')
router.register(r'groups', GroupViewSet, basename='groups')

urlpatterns = [
    path('v1/api-token-auth/', auth.obtain_auth_token, name='authtoken'),
    path('v1/', include(router.urls), name='router_v1')
]
