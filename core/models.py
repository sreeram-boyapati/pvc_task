import datetime
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
    created_at = models.DateTimeField()

    def cv_user_(self):
        if self.user is None:
            return None
        else:
            return self.user

    cv_user = property(cv_user_)

    def __unicode__(self):
        user = self.cv_user_()
        if user is None:
            return "Anonymous User"
        return user.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.datetime.now()
        return super(Job, self).save(*args, **kwargs)


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
    timestamp = models.DateTimeField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = datetime.datetime.now()
        return super(AbstractTask, self).save(*args, **kwargs)


class FetchTask(AbstractTask):
    """
     Fetch Images for a category.
    """
    # Foreign key is a nasty directed graph of relationship,
    # If a PhotoCategory is deleted, It will delete your FetchTask by virtue of
    # cascade delete by default, FetchTask should not be deleted
    # because its your stats data.
    category_id = models.PositiveIntegerField(default=0)
    cost_incurred = models.BooleanField(default=False)

    def get_category(self):
        # Handling a try/except is costly, better to use filter than get.
        photo_cat_set = PhotoCategory.objects.filter(id=self.category_id)
        if photo_cat_set:
            return photo_cat_set[0]
        return None

    category = property(get_category)

    def __unicode__(self):
        photo_category = self.get_category()
        if photo_category:
            return "{category}-{costed}".format(
                category=photo_category.category,
                costed=unicode(self.cost_incurred))
        else:
            return "Anonymous Fetch Task Anamoly!"

class TrainTask(AbstractTask):
    """
    Many models can be used to train a Image.
    Which one will be used here?
    Will add some stats here.
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
