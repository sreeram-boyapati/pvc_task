import os
import urllib
import uuid

from itertools import chain

from django.db import models
from django.core.files import File
from django.contrib.auth.models import User


def photo_upload_path(instance, filename):
    random = str(uuid.uuid1())
    random = random[:7]
    filename = random + filename
    return os.path.join('photos', filename)


# Create your models here.
class Photo(models.Model):
    photo_url = models.URLField(max_length=512)
    image = models.ImageField(upload_to=photo_upload_path,
                              null=True,
                              blank=True)

    def save(self, *args, **kwargs):
        if self.photo_url and not self.image:
            result = urllib.urlretrieve(self.photo_url)
            self.image.save(
                os.path.basename(self.photo_url),
                File(open(result[0]))
            )
        super(Photo, self).save(*args, **kwargs)

    def __unicode__(self):
        files_list = self.photo_url.split('/')
        return files_list[-1]


class Job(models.Model):
    """
        Describes a job.
    """
    user = models.ForeignKey(User, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def cv_user_(self):
        if self.user is None:
            return "Anonymous User"
        else:
            return self.user

    cv_user = property(cv_user_)


class PhotoCategory(models.Model):
    category = models.CharField(max_length=256, db_index=True)
    # Foreign key is a nasty relationship.
    photos = models.ManyToManyField(Photo)

    def __unicode__(self):
        return self.category


class AbstractTask(models.Model):
    """
    SubTasks of a job.
    """
    job = models.ForeignKey(Job)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class FetchTask(AbstractTask):
    """
     Fetch Images for a category.
    """
    category = models.ForeignKey(PhotoCategory)
    cost_incurred = models.BooleanField(default=False)


class TrainTask(AbstractTask):
    """
    Many models can be used to train a Image.
    Which one will be used here?
    """
    train_model = models.CharField(max_length=256)


class TestTask(AbstractTask):
    """
    Test this model.
    """
    test_model = models.CharField(max_length=256)


def get_all_tasks(job_id):
    fetch_tasks = FetchTask.objects.filter(id=job_id)
    train_tasks = TrainTask.objects.filter(id=job_id)
    test_tasks = TestTask.objects.filter(id=job_id)

    return list(chain(fetch_tasks, train_tasks, test_tasks))
