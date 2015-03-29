# Create your views here.
import json
import os

from django.conf import settings
from django.http import HttpResponse
from django.template import Template, Context

def get_homepage(resquest):
    template_name = "homepage.html"
    kwargs = {
    }
    context = Context(**kwargs)
    html_text = render_to_string(template_name,
                                 context)
    return HttpResponse(html_text)
