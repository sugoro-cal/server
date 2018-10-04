from django.urls import path
from .views import ProfileView, ProfileUpdateView


urlpatterns = [
    path("<uuid:pk>/", ProfileView.as_view(), name="profile"),
    path("change/<uuid:pk>/", ProfileUpdateView.as_view(), name="change_profile"),
]