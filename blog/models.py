from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            count = 0
            slug = slugify(self.name)
            while Category.objects.filter(slug=slug).exists():
                count += 1
                slug = f"{slug}-{count}"
            self.slug = slug
        super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            count = 0
            slug = slugify(self.name)
            while Tag.objects.filter(slug=slug).exists():
                count += 1
                slug = f"{slug}-{count}"
            self.slug = slug
        super(Tag, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, related_name='tag_posts')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    meta_title = models.CharField(max_length=200, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    meta_keywords = models.CharField(max_length=200, null=True, blank=True)
    description = RichTextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)
    published_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='published_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.IntegerField(default=0)
    userLikes = models.ManyToManyField(User, blank=True, related_name='post_likes')


    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    @property
    def is_published(self):
        return self.published_at is not None

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{count}'
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)


    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.comment} on {self.post}'
