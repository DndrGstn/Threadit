from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Post, Comment, Community
from .forms import RegisterForm, PostForm, CommentForm, CommunityForm


def home(request):
    """Home page showing all recent posts with optional search."""
    query = request.GET.get("q", "")
    posts = Post.objects.select_related("author", "community").all()

    if query:
        # Filter posts by title or body containing the search term
        posts = posts.filter(Q(title__icontains=query) | Q(body__icontains=query))

    communities = Community.objects.all()[:8]
    context = {"posts": posts, "communities": communities, "query": query}
    return render(request, "forum/home.html", context)


def community_detail(request, name):
    """Show all posts in a specific community."""
    community = get_object_or_404(Community, name=name)
    posts = Post.objects.filter(community=community).select_related("author")
    context = {"community": community, "posts": posts}
    return render(request, "forum/community.html", context)


def post_detail(request, pk):
    """Show a single post and its comments."""
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post, parent=None).prefetch_related(
        "replies__author", "author"
    )
    form = CommentForm()

    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            # Handle reply to another comment
            parent_id = request.POST.get("parent_id")
            if parent_id:
                comment.parent = get_object_or_404(Comment, pk=parent_id)
            comment.save()
            messages.success(request, "Comment added!")
            return redirect("post_detail", pk=pk)

    context = {"post": post, "comments": comments, "form": form}
    return render(request, "forum/post_detail.html", context)


@login_required
def create_post(request):
    """Create a new post."""
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created!")
            return redirect("post_detail", pk=post.pk)

    context = {"form": form, "title": "Create Post"}
    return render(request, "forum/post_form.html", context)


@login_required
def edit_post(request, pk):
    """Edit an existing post — only the author can do this."""
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, "You can only edit your own posts.")
        return redirect("post_detail", pk=pk)

    form = PostForm(instance=post)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated!")
            return redirect("post_detail", pk=pk)

    context = {"form": form, "title": "Edit Post", "post": post}
    return render(request, "forum/post_form.html", context)


@login_required
def delete_post(request, pk):
    """Delete a post — only the author can do this."""
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        messages.error(request, "You can only delete your own posts.")
        return redirect("post_detail", pk=pk)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect("home")

    return render(request, "forum/confirm_delete.html", {"post": post})


@login_required
def create_community(request):
    """Create a new community."""
    form = CommunityForm()
    if request.method == "POST":
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.created_by = request.user
            community.save()
            messages.success(request, f"r/{community.name} created!")
            return redirect("community_detail", name=community.name)

    return render(request, "forum/community_form.html", {"form": form})


def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect("home")

    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect("home")

    return render(request, "forum/register.html", {"form": form})


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "forum/login.html", {})


def logout_view(request):
    """Log the user out."""
    logout(request)
    return redirect("home")
