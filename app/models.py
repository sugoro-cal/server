from django.db import models
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    name = models.CharField(default=_("guest_user"), max_length=63)
    addr = models.CharField(default=_("山口県周南市学園台"), max_length=63)
