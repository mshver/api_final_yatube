from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework import filters
from rest_framework import pagination
from rest_framework.serializers import ValidationError
from posts.models import (
    Post, Comment, Group, Follow
)
from .serializers import (
    PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
)


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer: PostSerializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        filter = {}
        for field in self.kwargs:
            filter[field] = self.kwargs[field]
        return Comment.objects.filter(**filter)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('following__username',)

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

    def perform_create(self, serializer: FollowSerializer):
        following_username = self.request.data.get('following')
        if following_username:
            following_user = get_object_or_404(User,
                                               username=following_username)
            serializer.save(user=self.request.user,
                            following=following_user)
        else:
            raise ValidationError('following is empty')
