from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator
from django.core.mail import send_mail
from .forms import EmailPostForm, CommentForm, SearchForm
from django.contrib import messages
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector



def list_post(request, tag_slug=None):
    posts = Post.pubed.all()
    tag = None
    if tag_slug:
        
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.pubed.filter(tags__in=[tag])
    paging = Paginator(posts, 3)
    page = request.GET.get('page', 1)
    page_obj = paging.page(page)

    return render(request, 'blog/post/list.html', {'posts':page_obj, 'tag': tag})

def detail_post(request, slug, year, month, day):
    post = get_object_or_404(Post, slug=slug, publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    Ptags = post.tags.all()
    similar_posts = Post.pubed.filter(tags__in=Ptags).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid:
            new_com = form.save(commit=False)
            new_com.user = request.user
            new_com.post = post
            new_com.save()
            messages.success(request, 'great you have added a comment succefully')
            form = CommentForm()
    else:
        form = CommentForm()
    
    return render(request, 'blog/post/detail.html', {'post': post, 'form': form, 'comments': comments, 'similar_posts': similar_posts})

def shar_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            email = cd ['email']
            to = cd['to']
            comment = cd['comment']
            send_mail(post.title, f'we want you to read this post{comment} by {name}', email, [to] )
            messages.success(request, 'great you have completed sent it')
    else:
        form = EmailPostForm()      
    return render(request, 'blog/post/share.html', {'form': form, 'post': post})  


def post_search(request):
    form = SearchForm()
    q = None
    results = []
    if 'q' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            results = Post.pubed.annotate(search=SearchVector('title', 'body'),).filter(search=q)
            # results = Post.pubed.annotate(search=SearchVector('title', 'body'),).filter(search=query)
    return render(request,'blog/post/search.html',{'form': form,'q': q,'results': results})        

