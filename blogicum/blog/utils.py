from django.utils import timezone
from django.db.models import Count
from django.core.paginator import Paginator

from blog.models import Category, Post


def query_post(user=Post.objects,
               filters=True,
               comments=True):

    query_set = (
        user.select_related(
            'category',
            'location',
            'author',
        )
    )
    if filters:
        query_set = query_set.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )
    if comments:
        query_set = query_set.annotate(comments_cout=Count('comments'))
    return query_set


def query_category():
    query_set = Category.objects.filter(
        is_published=True
    )
    return query_set


def posts_pagination(request, posts):

    page_num = request.GET.get(
        'page', 1
    )
    paginator = Paginator(posts, 10)
    return paginator.get_page(page_num)
