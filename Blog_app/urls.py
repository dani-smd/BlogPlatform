from django.urls import path, include
from rest_framework import routers
# ---
from Blog_app.Posts.views import PostViewSet
from Blog_app.Rate.views import RateBlogView

router = routers.DefaultRouter()
router.register(r'blog-post', PostViewSet)

rate_list = RateBlogView.as_view({'get': 'list'})
rate_create = RateBlogView.as_view({'post': 'create'})

app_name = "Blog_app"
urlpatterns = [
    path('', include(router.urls)),
    path('rate/<int:pk>/', rate_list, name='rate-list'),
    path('rate/', rate_create, name='rate-create'),
]
