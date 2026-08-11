from django.urls import path
from . import views

urlpatterns = [
    path('post/new/', views.create_post, name='create_post'),
    path('', views.feed, name='feed'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
]