from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('event_info/<int:pk>/', views.EventInfoView.as_view(), name="event_info"),
    path('registration_for_shops/', views.RegisterForShopsView.as_view(), name='register_for_shops'),
    path(
        'registration_for_participates/<int:pk>/',
        views.RegisterForParticipatesView.as_view(),
        name='register_for_participates'
    ),
    path('shop_entry/<int:pk>/', views.ShopEntryView.as_view(), name='shop_entry'),
    path('participate_entry/<int:pk>/', views.ParticipateEntryView.as_view(), name='participate_entry'),
]
