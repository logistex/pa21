from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='user_photos')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d',
                              default='photos/no_image.png')
                              # default='http://placehold.it/800x600?text=blank')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + "님이 " \
               + self.created.strftime("%Y-%m-%d %H:%M:%S") + "에 등록한 사진"

    def get_absolute_url(self):
        return reverse('photo:photo_detail', args=[str(self.id)])