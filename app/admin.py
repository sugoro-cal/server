from django.contrib import admin
from .models import Event

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    field = [
        "registration_state",
        "address",
        "date",
        "event_content"
    ]
    list_display = [
        "registration_state",
        "address",
        "date",
        "event_content"
    ]
