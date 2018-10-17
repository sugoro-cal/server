from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import ProfileView, ProfileUpdateView


urlpatterns = [
    path("<uuid:pk>/", login_required(ProfileView.as_view()), name="profile"),
    path("change/<uuid:pk>/", login_required(ProfileUpdateView.as_view()), name="change_profile"),
]
