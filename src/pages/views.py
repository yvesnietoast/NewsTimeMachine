import os

from django import get_version
from django.conf import settings
from django.shortcuts import render
from news.models import newsBit

def home(request):
    context = {
        "debug": settings.DEBUG,
        "django_ver": get_version(),
        "python_ver": os.environ["PYTHON_VERSION"],
    }

    return render(request, "pages/home.html", context)

def latest(request):
    newsBits= newsBit.objects.all()
    return render(request,"pages/test.html",{'newsBits':newsBits})