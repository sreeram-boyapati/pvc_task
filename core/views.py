import json
import os

from django.conf import settings
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import render_to_string

from core.models import Photo, PhotoCategory, Job
from core.models import FetchTask
from utilityapp import flickerstream


def render_string(template_string, context):
    """
    String written in django template language is populated with context.
    """
    t = Template(template_string)
    c = Context(context)
    return t.render(c)


def get_relative_path(location_url):
    """
    remove media root
    """
    media_root = settings.MEDIA_ROOT
    return os.path.relpath(location_url, media_root)


def get_or_create_job(request):
    job = None
    print request.session
    if not request.session.get("job_id"):
        print "Job Found"
        job = Job()
        if request.user.id:
            job.user = request.user
        job.save()
        request.session.job_id = job.id
    else:
        job_id = request.session["job_id"]
        job = Job.objects.get(id=job_id)
        if job.user is None and request.user is not None:
            # a user has registered. create a new job id for him.
            print "New Job for user"
            job = Job()
            job.user = request.user
            job.save()
            request.session.job_id = job.id
    return job


def fetch_images(request, category):
    """
        Render images in the back.
    """
    response = {}
    if category is None:
        response.update({
            "status": "ERROR",
            "html_text": "Category is not Found.",
        })
        return HttpResponse(json.dumps(response),
                            content_type="application/json")

    tags = [category]
    photos = []

    job = get_or_create_job(request)
    photo_cat_set = PhotoCategory.objects.filter(category=category)
    photo_category = None

    if photo_cat_set:
        photo_category = photo_cat_set[0]
        photos = photo_category.photos.all()
        f_task = FetchTask(job=job, category_id=photo_category.id)
        f_task.save()
    else:
        # Downloading images
        photo_category = PhotoCategory(category=category)
        photo_tuples = flickerstream.fetch_request(tags)
        photo_category.save()
        f_task = FetchTask(job=job,
                           category_id=photo_category.id,
                           cost_incurred=True)
        f_task.save()
        for each_url in photo_tuples:
            photo = Photo(photo_url=each_url)
            photo.save()
            photo_category.photos.add(photo)
            photos.append(photo)

    context = Context({
        "photos": photos
    })
    response["html_text"] = render_to_string("images_list.html", context)
    response["status"] = "OK"
    return HttpResponse(json.dumps(response), content_type="application/json")
