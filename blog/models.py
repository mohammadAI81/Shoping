from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class SortByDateTimeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-datetime_created')


class PublishedBlogManager(models.Manager):
    def blog_published(self):
        return self.get_queryset().filter(published=True)


class Blog(models.Model):
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField()
    published = models.BooleanField(default=True)

    datetime_created = models.DateTimeField(auto_now_add=True, editable=True)
    datetime_modified = models.DateTimeField(auto_now=True, editable=True)

    objects = SortByDateTimeManager()
    object_published = PublishedBlogManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def get_ablosute_url(self):
        return reverse('blog:blog', args=[self.slug])


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    email = models.EmailField()
    description = models.TextField()

    datetime_created = models.DateTimeField(auto_now_add=True, editable=True)
    datetime_modified = models.DateTimeField(auto_now=True, editable=True)

    objects = SortByDateTimeManager()

    def __str__(self):
        return f'{self.author} comment for {self.blog.title}'
