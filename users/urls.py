from django.urls import path
from .views import ProfileView


urlpatterns = [
    path("<uuid:pk>/", ProfileView.as_view(), name="profile"),
]