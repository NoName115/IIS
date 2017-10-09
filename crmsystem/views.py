from django.shortcuts import render


def default_web(request):
    return render(request, 'crmsystem/base.html', {})
