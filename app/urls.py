from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('event_info/<int:pk>/', views.EventInfoView.as_view(), name="event_info"),
    path('registration_shops/', login_required(views.RegisterShopsView.as_view()), name='register_shops'),
    path(
        'registration_participates/<int:pk>/',
        views.RegisterParticipatesView.as_view(),
        name='register_participates'
    ),
    path(
        'finish_participate_entry/<int:pk>/',
        login_required(views.finish_to_register_participates_view),
        name='finish_participate_entry'
    ),
    path('shop_entry/<int:pk>/', login_required(views.ShopEntryView.as_view()), name='shop_entry'),
    path('participate_entry/<int:pk>/', login_required(views.participate_entry), name='participate_entry'),
]
