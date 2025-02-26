from django.urls import re_path

from . import views

app_name = "flex_blob"

urlpatterns = [
    re_path(
        r"^(?P<path>.*)$",
        views.MediaView.as_view(),
        name="media",
    )
]
