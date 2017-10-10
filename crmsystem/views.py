from django.shortcuts import render
from django.utils import timezone
from .models import *


def default_web(request):
    return render(request, 'crmsystem/base.html', {})
