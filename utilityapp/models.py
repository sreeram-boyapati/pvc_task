import os
import urllib

from django.db import models
from django.core.files import File


# Create your models here.
class Photo(models.Model):
    file_url = models.TextField(unique=True)
    image = models.ImageField(upload_to='/media/', blank=True)

    def cache(self):
        """Store image locally if we have a URL"""

        if self.url and not self.image:
            result = urllib.urlretrieve(self.url)
            self.image.save(
                os.path.basename(self.url),
                File(open(result[0])),
            )
            self.save()

    def __unicode__(self):
        files_list = self.file_url.split('/')
        return files_list[-1]


class PhotoCategory(models.Model):
    category = models.CharField(max_length=256)
    photo = models.ForeignKey(Photo)

    def __unicode__(self):
        return self.category + " " + self.photo.__unicode__()
