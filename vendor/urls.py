from django.urls import path

from accoounts.views import vendor_dashboard

from . import views

urlpatterns = [
    path("", vendor_dashboard),
    path("profile/", views.v_profile, name="v_profile"),
]
