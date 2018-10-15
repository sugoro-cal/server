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
        model = models.Event
        fields = (
            'delegation_name',
            'shop_name',
            'address',
            'mail'
        )


# TODO 一般ユーザ向け参加者登録ページのフォーム
class ParticipateEntryForm(forms.ModelForm):
    pass