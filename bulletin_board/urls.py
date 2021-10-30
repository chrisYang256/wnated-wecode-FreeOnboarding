from django.urls import path

from .views import Post, PostDetail

urlpatterns = [
    path('/post', Post.as_view()),
    path('/post/<int:post_id>', Post.as_view()),
    path('/post-detail/<int:post_id>', PostDetail.as_view()),
]