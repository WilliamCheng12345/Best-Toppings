from django.urls import path
from .views import (
    PostsListView,
    PostsDetailView,
    PostsCreateView,
    PostsEditView,
    PostsDeleteView,
    CommentsCreateView,
    CommentsDeleteView,
    CommentsEditView
)

urlpatterns = [
    path('<int:postpk>/<int:pk>/deleteComment/', CommentsDeleteView.as_view(), name='comments_delete'),
    path('<int:postpk>/<int:pk>/editComment/', CommentsEditView.as_view(), name='comments_edit'),
    path('<int:pk>/newComment/', CommentsCreateView.as_view(), name='comments_new'),
    path('<int:pk>/deletePost/', PostsDeleteView.as_view(), name='posts_delete'),
    path('<int:pk>/editPost/', PostsEditView.as_view(), name='posts_edit'),
    path('newPost/', PostsCreateView.as_view(), name='posts_new'),
    path('<int:pk>/', PostsDetailView.as_view(), name='posts_detail'),
    path('', PostsListView.as_view(), name='posts_list'),
]
