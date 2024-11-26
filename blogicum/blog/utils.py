from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone

from blog.models import Post


def posts_pagination(request, posts):
    page_number = request.GET.get(
        'page',
        1
    )
    paginator = Paginator(posts, 10)
    return paginator.get_page(page_number)


def query_post(
        manager=Post.objects,
        filters=True,
        with_comments=True
):
    queryset = manager.select_related('author', 'location', 'category')
    if filters:
        queryset = queryset.filter(
            is_published=True,
            pub_date__lt=timezone.now(),
            category__is_published=True
        )
    if with_comments:
        queryset = queryset.annotate(comment_count=Count('comments'))
    return queryset.order_by('-pub_date')
