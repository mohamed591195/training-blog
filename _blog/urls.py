from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap
from .feeds import LatestPostsFeed

sitemaps = {
    'posts': PostSitemap
}

app_name = 'blog'

urlpatterns = [
    path('', views.list_post, name='post_list_page'),
    path('post/<slug:slug>/<int:year>/<int:month>/<int:day>/', views.detail_post, name='post_detail_page'),
    path('post/<int:id>/share/', views.shar_post, name='share_post_page'),
    path('posts/<slug:tag_slug>/', views.list_post, name='tagged_posts_page'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap'),
     path('feed/', LatestPostsFeed(), name='post_feed_page'),
     path('search/', views.post_search, name='post_search_page'),
]
