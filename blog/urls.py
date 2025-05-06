from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import signup_view

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),  # Signup page
    path('login/', views.login_view, name='login'),  # Login page (add later)
    path('logout/', views.logout_view, name='logout'),  # Logout page (add later)
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('signup/', views.signup_view, name='signup'),  # Register URL
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='blog/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_complete.html'), name='password_reset_complete'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
  

    path('', views.home, name='home'),
    path('search/', views.search_posts, name='search_posts'),  # Add this line
    path('create/', views.post_create, name='create_post'),
    path('post/new/', views.post_create, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.update_post, name='post_update'),
    path('post/<int:pk>/delete/', views.delete_post, name='post_delete'),  
    path('post/<int:pk>/edit/', views.update_post, name='update_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('search/', views.search_posts, name='search'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),


    
    
]
