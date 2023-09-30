from django.urls import path
# ---
from Comment_app.views import CommentViewSet

comment_list = CommentViewSet.as_view({'get': 'list'})
comment_delete = CommentViewSet.as_view({'delete': 'destroy'})

app_name = "Comment_app"
urlpatterns = [
    path('comment-post/<int:pk>/', comment_list, name='comment-list'),
    path('comment-delete/<int:pk>/', comment_delete, name='comment-delete'),
    path('comment-post/', CommentViewSet.as_view({'post': 'create', 'put': 'update'}), name='comment-post'),
]
