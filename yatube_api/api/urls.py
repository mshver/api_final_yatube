from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='post')
router.register('groups', views.GroupViewSet, basename='group')
router.register('follow', views.FollowViewSet, basename='follow')

commentsRouter = DefaultRouter()
commentsRouter.register('comments', views.CommentViewSet, basename='coment')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/posts/<int:post_id>/', include(commentsRouter.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
