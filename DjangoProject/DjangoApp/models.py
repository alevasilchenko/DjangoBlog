from django.db import models
from django.utils import timezone  # часовые пояса
from django.contrib.auth.models import User  # аутентификация пользователей
from django.urls import reverse


class PublishedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)  # заголовок статьи
    slug = models.SlugField(max_length=250, unique_for_date='publish')  # URL на основе уникальной даты публикации
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')  # внешний ключ "one-to-many"
    body = models.TextField()  # содержание статьи
    created = models.DateTimeField(auto_now_add=True)  # дата создания статьи
    updated = models.DateTimeField(auto_now=True)  # дата, когда статья была отредактирована
    publish = models.DateTimeField(default=timezone.now)  # дата публикации статьи
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='draft')  # статус статьи

    objects = models.Manager()  # менеджер по умолчанию
    published = PublishedManager()  # наш новый менеджер

    class Meta:  # метаданные в порядке убывания (префикс -)
        ordering = ('-publish',)

    def __str__(self):
        return self.title  # возвращает отображение, понятное для человека

    def get_absolute_url(self):
        return reverse('DjangoApp:post_detail',
                       args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

    def get_absolute_url(self):
        return reverse('DjangoApp:post_detail',
                       args=[self.post.publish.year, self.post.publish.month, self.post.publish.day, self.post.slug])
