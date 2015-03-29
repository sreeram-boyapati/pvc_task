# Create your views here.
import json
import os

from django.conf import settings
from django.http import HttpResponse
from django.template import Template, RequestContext
from django.template.loader import render_to_string

def get_homepage(request):
    template_name = "homepage.html"
    kwargs = {
    }
    context = RequestContext(request, **kwargs)
    html_text = render_to_string(template_name,
                                 context)
    return HttpResponse(html_text)
