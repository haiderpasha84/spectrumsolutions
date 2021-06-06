from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import timezone

from tinymce.widgets import TinyMCE
from tinymce.models import HTMLField
# Create your models here.

class AcceptedpostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class post(models.Model):
    post_id= models.AutoField(primary_key=True)
    title = models.CharField(max_length=255 ,default="")
    author =models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=130)
    timeStamp = models.DateTimeField()
    thumbnail = models.ImageField(upload_to='shop/images', default="")
    status=models.BooleanField(default="False")

    content = HTMLField()
    acceptpost = AcceptedpostManager()
    objects =models.Manager()

    def __str__(self):
        return self.title




