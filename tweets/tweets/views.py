from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')

    return HttpResponseForbidden("You are not logged in.")


def echo(request):
    headers_dict = {}
    for item in request.headers.items():
        headers_dict[item[0]] = item[1]

    return HttpResponse(str(headers_dict))