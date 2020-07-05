from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=50)
    content = models.TextField('Текст публикации', max_length=250)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('post_details', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.author} {self.title}'
