from django.urls import path
from django.contrib.auth import views as auth_views  # <-- Add this line
from . import views

urlpatterns = [
    # User authentication URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.post_create, name='create_post'), 
    path('update_post/<int:id>/', views.update_post, name='update_post'),


    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='blog/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_complete.html'), name='password_reset_complete'),

    # Blog post URLs
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.update_post, name='post_update'),
    path('post/<int:pk>/delete/', views.delete_post, name='post_delete'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),

    # API URLs
    path('api/posts/', views.PostListAPIView.as_view(), name='api-posts'),
    path('api/posts/<int:pk>/', views.PostDetailAPIView.as_view(), name='api-post-detail'),
    path('api/comments/', views.CommentListCreateAPIView.as_view(), name='api-comments'),
]
