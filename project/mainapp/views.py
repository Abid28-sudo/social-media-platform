from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CommentForm, PostForm, Register
from .models import Follow, Like, Post


def home(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('login')


def signup(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = Register()
    return render(request, 'mainapp/signup.html', {'form': form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'mainapp/create_post.html', {'form': form})
    

@login_required
def feed(request):
    posts = Post.objects.all()
    return render(request,'mainapp/feed.html',{'posts':posts})

@login_required
def post_detail(request,post_id):
    post = get_object_or_404(Post,id = post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    user_has_liked = post.likes.filter(user=request.user).exists()

    return render(request, 'mainapp/post_detail.html',
                  {'post': post, 'form': form, 'user_has_liked': user_has_liked})

@login_required
def toggle_like(request,post_id):
    post = get_object_or_404(Post,id = post_id)
    like, created = Like.objects.get_or_create(post = post, user = request.user)
    if not created:
        like.delete()
    return redirect('post_detail',post_id  = post.id)

@login_required
def toggle_follow(request,username):
    target_user = get_object_or_404(User,username = username)
    if target_user == request.user:
        return redirect('profile',username = username)

    follow,created = Follow.objects.get_or_create(follower = request.user , following = target_user)
    if not created:
        follow.delete()
    return redirect('profile',username = username)    

@login_required
def profile(request,username):
    profile_user = get_object_or_404(User,username = username)    
    posts = profile_user.posts.all()
    is_following = Follow.objects.filter(follower = request.user , following = profile_user).exists()
    
    return render(request,'mainapp/profile.html',{
        'profile_user': profile_user,
        'posts':posts,
        'is_following': is_following,
        'followers_count':profile_user.followers.count(),
        'following_count':profile_user.following.count(),
    })