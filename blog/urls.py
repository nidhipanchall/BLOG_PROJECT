from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import PostListCreateAPIView, PostDetailAPIView, PostRetrieveUpdateDestroyAPIView

urlpatterns = [
    # User authentication URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.post_create, name='create_post'), 
    path('update_post/<int:pk>/', views.update_post, name='update_post'),
    path('search/', views.search_view, name='search'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'), 
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/', views.post_list, name='post_list'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', views.profile_view, name='profile'),

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
    path('api/posts/', PostListCreateAPIView.as_view(), name='api-posts'), 
    # path('api/posts/<int:pk>/', PostDetailAPIView.as_view(), name='api-post-detail'),
    path('api/comments/', views.CommentListCreateAPIView.as_view(), name='api-comments'),
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    # path('posts/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),
    path('api/posts/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail-update-delete')
    


]
