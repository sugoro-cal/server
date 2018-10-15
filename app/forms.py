from django import forms

from . import models


class EventRegisterForShopForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = (
            'event_name',
            'mail',
            'address',
            'date',
            'event_content',
        )


class EventRegisterForParticipateForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = (
            'event_name',
            'mail',
            'address',
            'date',
            'event_content',
            'participating_shops_text',
            'original',
        )


class ShopEntryForm(forms.ModelForm):

    class Mata:
        pass