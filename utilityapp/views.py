import flickerstream
import json
import os

from django.conf import settings
from django.http import HttpResponse
from django.template import Template, Context

from utilityapp.models import Photo, PhotoCategory


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
    photo_tuples = flickerstream(tags)
    photos = []
    for each_photo in photo_tuples:
        photo = Photo(url=photo[0],
                      image=get_relative_path(photo[1]))
        photo.save()
        photos.append(photo)
    html_text = render_string("image_list.html", photos)
    return HttpResponse(json.dumps(response), content_type="application/json")
