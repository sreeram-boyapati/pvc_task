import os
import urllib

from django.db import models
from django.core.files import File


# Create your models here.
class Photo(models.Model):
    photo_url = models.TextField(unique=True)
    image = models.ImageField(upload_to='', blank=True)

    def __unicode__(self):
        files_list = self.photo_url.split('/')
        return files_list[-1]


class PhotoCategory(models.Model):
    category = models.CharField(max_length=256)
    photo = models.ForeignKey(Photo)

    def __unicode__(self):
        return self.category + " " + self.photo.__unicode__()
