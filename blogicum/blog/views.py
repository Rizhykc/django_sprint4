from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from blog.constants import POSTS_MAIN_PAGE
from blog.forms import CommentForm, PostForm, ProfileForm
from blog.models import Comment, Post
from blog.utils import posts_pagination, query_category, query_post


def index(request):

    post_list = query_post().order_by('-pub_date')[:POSTS_MAIN_PAGE]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def category_posts(request, category_slug):

    category = get_object_or_404(
        query_category(),
        slug=category_slug,
    )
    post_list = (
        query_post()
        .filter(category=category)
        .order_by("-pub_date")
    )
    context = {'category': category, 'post_list': post_list}
    return render(request, 'blog/category.html', context)


def post_detail(request, id):

    post_list = get_object_or_404(
        query_post(),
        pk=id,
    )
    context = {'post': post_list}
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
    if profile == request.user:
        posts = query_post(user=profile.posts, filters=False)
    else:
        posts = query_post(user=profile.posts)
    object_page = posts_pagination(request, posts)
    context = {
        'profile': profile,
        'object_page': object_page
    }
    return render(request, 'blog/profile.html', context)


def edit_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/user.html', {'form': form})

# class ProfileListView(ListView):
#     model = User
#     template_name = 'blog/profile.html'
#     ordering = 'id'
#     paginate_by = 10

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["profile"] = get_object_or_404(
#             User,
#             username=self.kwargs.get('username')
#         )
#         return context
