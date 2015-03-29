import flickerstream
import uuid
import json
import os

from django.conf import settings
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import render_to_string

from core.models import Photo, PhotoCategory


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

def  get_or_create_job(request, job_id):
    job = None
    if request.session["job_id"] is None:
        job = Job()
        if request.user:
            job.user = user
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
    photo_tuples = flickerstream(tags)
    photos = []

    photo_category = PhotoCategory(category=category)
    photo_category.save()

    for each_photo in photo_tuples:
        photo = Photo(url=each_photo[0],
                      image=get_relative_path(each_photo[1]))
        photo.save()
        photo_category.photos.add(photo)
        photos.append(photo)
    response["html_text"] = render_to_string("image_list.html", photos)
    response["status"] = "OK"

    return HttpResponse(json.dumps(response), content_type="application/json")
