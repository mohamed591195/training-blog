from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager

class pub_posts(models.Manager):
    def get_queryset(self):
        return super(pub_posts, self).get_queryset().filter(status='puplished')

class Post(models.Model):
    STATUS_CHOICES = (( 'puplished', 'P'), ('draft', 'D'))
    title = models.CharField(max_length=200)
    slug  = models.SlugField(max_length=200, unique_for_date='publish')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=200, default='draft')
    tags = TaggableManager()
    objects = models.Manager()
    pubed = pub_posts()
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.slug)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail_page', kwargs={'slug':self.slug, 
                                                              'year': self.publish.year,
                                                              'month': self.publish.month,
                                                              'day':self.publish.day})
    class Meta:
        ordering = ['-publish']
    
    def __str__(self):
        return self.title

     
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='his_comments')
    body = models.TextField()   
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return 'commont by {} on {}'.format(self.user, self.post)