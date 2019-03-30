from django.template import Library
from ..models import Post
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe
register = Library()


@register.simple_tag
def total_posts():
    return Post.pubed.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.pubed.all().order_by('-publish')[:count]

    return {'latest_posts': latest_posts}

@register.simple_tag
def most_commented_posts(count=3):
    return Post.pubed.annotate(num_comments=Count('comments')).order_by('-num_comments')[:count]

@register.filter(name='markdown')
def markdown_filter(text):
    return mark_safe(markdown.markdown(text))