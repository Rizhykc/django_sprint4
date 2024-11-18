from django.shortcuts import get_object_or_404, render

from blog.constants import POSTS_MAIN_PAGE
from blog.utils import query_category, query_post


def index(request):

    post_list = query_post().order_by('-pub_date')[:POSTS_MAIN_PAGE]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, id):

    post_list = get_object_or_404(
        query_post(),
        pk=id,
    )
    context = {'post': post_list}
    return render(request, 'blog/detail.html', context)


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
