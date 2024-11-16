from django.http.request import HttpRequest

from . import models


def username_badge(request: HttpRequest):
    return request.user.username, "success"


def courses_count(request: HttpRequest):
    return models.Course.objects.count()


def places_count(request: HttpRequest):
    return models.Place.objects.count()


def phones_count(request: HttpRequest):
    return models.Phone.objects.count()


def links_count(request: HttpRequest):
    return models.Link.objects.count()


def users_count(request: HttpRequest):
    return models.TGUser.objects.count()


def texts_count(request: HttpRequest):
    return models.Text.objects.count()
