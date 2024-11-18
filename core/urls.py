from django.urls import path
from django.conf import settings
from django.views.generic import RedirectView


urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url=f"{settings.STATIC_URL}favicon.ico", permanent=True)),
]
