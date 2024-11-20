from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('posts/create/', views.create_posts, name='create_post'),
    path('posts/<int:id>/edit/', views.edit_posts, name='edit_post'),
    path('posts/<int:id>/delete/', views.delete_posts, name='delete_post'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('profile/edit_profile/', views.edit_profile, name='edit_profile'),
]
