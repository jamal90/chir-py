from django.shortcuts import render
from django.http import HttpResponseForbidden


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')

    return HttpResponseForbidden("You are not logged in.")