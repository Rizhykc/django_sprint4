from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from blog.forms import CommentForm, PostForm, ProfileForm
from blog.models import Comment, Post
from blog.utils import posts_pagination, query_category, query_post


# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import UpdateView
# from django.urls import reverse, reverse_lazy



def index(request):

    page_obj = posts_pagination(request, query_post(
        filters=True,
        comments=True
    ))
    context = {'page_obj':page_obj}
    return render(request, 'blog/index.html', context)


def category_posts(request, category_slug):

    category = get_object_or_404(
        query_category(),
        slug=category_slug,
    )
    page_obj = posts_pagination(
        request,
        query_post(user=category.posts)
    )
    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'blog/category.html', context)


def post_detail(request, id):

    post = get_object_or_404(
        Post,
        pk=id,
    )
    if post.author != request.user:
        post = get_object_or_404(query_post(), id=id)
    comments = Comment.objects.select_related('author').filter(post=post)
    form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'blog/detail.html', context)


@login_required
def create_posts(request):

    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', request.user)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def edit_posts(request, id_post):

    post = get_object_or_404(Post, id=id_post)
    if request.user != post.author:
        return redirect('blog:post_detail', id_post)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', id_post)
    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def delete_posts(request, id_post):

    post = get_object_or_404(Post, id=id_post)
    if request.user != post.author:
        return redirect('blog:post_detail', id_post)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    context = {'form': form}
    return render(request, 'blog/create.html', context)


def profile(request, username):

    profile = get_object_or_404(User, username=username)
    posts = query_post(user=profile.posts) if profile != request.user else query_post(user=profile.posts, filters=False)

    page_obj = posts_pagination(request, posts)
    context = {
        'profile': profile,
        'page_obj': page_obj,
    }

    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):

    form = ProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/user.html', {'form': form})


@login_required
def add_comment(request, id_post):
    """Добавление комментария публикации."""
    post = get_object_or_404(Post, id=id_post)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', id=id_post)



@login_required
def edit_comment(request, id_post, id_comment):

    comment = get_object_or_404(Comment,
                                id=id_comment,
                                post_id=id_post,
                                author=request.user)
    form = CommentForm(request.POST or None, instance=comment)
    context = {'form': form, 'comment': comment}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', id=id_post)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, id_post, id_comment):

    comment = get_object_or_404(Comment,
                                id=id_comment,
                                post_id=id_post,
                                author=request.user)
    context = {'comment': comment}
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', id=id_post)
    return render(request, 'blog/comment.html', context)
