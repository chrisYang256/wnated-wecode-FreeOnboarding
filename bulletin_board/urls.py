from django.urls import path

from .views import PostList, PostDetail, PostWrite, PostUpdate, PostDelete

urlpatterns = [
    path('/post-list', PostList.as_view()),
    path('/post-detail/<int:post_id>', PostDetail.as_view()),
    path('/post-write', PostWrite.as_view()),
    path('/post-update/<int:post_id>', PostUpdate.as_view()),
    path('/post-delete/<int:post_id>', PostDelete.as_view()),
]