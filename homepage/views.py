from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string

from core.forms import SignupForm


def get_homepage(request):
    template_name = "homepage.html"
    kwargs = {
    }
    context = RequestContext(request, **kwargs)
    html_text = render_to_string(template_name,
                                 context)
    return HttpResponse(html_text)


def signup_view(request):
    template_name = "signup.html"
    form = SignupForm()
    kwargs = {
        "signup_form": form,
    }
    context = RequestContext(request, **kwargs)
    html_text = render_to_string(template_name, context)
    return HttpResponse(html_text)
