from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Post, Comment, Like, Profile
from .forms import PostForm, CommentForm, ProfileForm
from django.utils import timezone
from django.contrib import messages
from rest_framework import generics, permissions
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from rest_framework.permissions import IsAuthenticatedOrReadOnly


# Home view
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': posts})

def search_posts(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=query) if query else Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.updated_at = timezone.now()
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def update_post(request, pk):  
    post = get_object_or_404(Post, pk=pk)
    
    if post.author != request.user:
        messages.error(request, "You do not have permission to edit this post.")
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_at = timezone.now()
            post.save()
            messages.success(request, "Post updated successfully!")
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {'form': form, 'post': post})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    has_liked = post.likes.filter(user=request.user).exists() if request.user.is_authenticated else False

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'has_liked': has_liked,
    })

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blog/confirm_delete.html', {'post': post})

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not Like.objects.filter(user=request.user, post=post).exists():
        Like.objects.create(user=request.user, post=post)
    return redirect('post_detail', pk=post.id)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'blog/profile.html', {
        'form': form,
        'profile': profile,
    })

@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'blog/profile.html', {'form': form, 'profile': profile})

def search_view(request):
    query = request.GET.get('q')
    results = Post.objects.filter(title__icontains=query) if query else []
    return render(request, 'blog/search_results.html', {'results': results, 'query': query})

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})


# API views
class PostListCreateAPIView(generics.ListCreateAPIView):  
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        print("PUT request received")
        return super().put(request, *args, **kwargs)

class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
