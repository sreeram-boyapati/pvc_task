import json
import os

from django.conf import settings
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import render_to_string

from core.models import Photo, PhotoCategory, Job
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


def get_or_create_job(request, job_id):
    job = None
    if request.session["job_id"] is None:
        job = Job()
        if request.user:
            job.user = request.user
        job.save()
    else:
        job = Job.objects.get(id=job_id)


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

    # Generate job Ids

    tags = [category]
    photos = []
    photo_cat_set = PhotoCategory.objects.filter(category=category)
    photo_category = None
    if photo_cat_set:
        photo_category = photo_cat_set[0]
        photos = photo_category.photos.all()
    else:
        photo_category = PhotoCategory(category=category)
        photo_tuples = flickerstream.fetch_request(tags)
        photo_category.save()
        for each_url in photo_tuples:
            photo = Photo(photo_url=each_url)
            photo.save()
            photo_category.photos.add(photo)
            photos.append(photo)
    context = Context({
        "photos": photos
    })
    print photos
    response["html_text"] = render_to_string("images_list.html", context)
    response["status"] = "OK"
    print response
    return HttpResponse(json.dumps(response), content_type="application/json")
