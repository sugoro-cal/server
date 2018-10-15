from django.urls import path

from . import views


urlpatterns = [
    path('event_info/<int:pk>/', views.EventInfoView.as_view(), name="event_info"),
    path('registration_for_shops/', views.RegisterForShopsView.as_view(), name='register_for_shops'),
    path(
        'registration_for_participates/<int:pk>/',
        views.RegisterForParticipatesView.as_view(),
        name='register_for_participates'
    ),
]
