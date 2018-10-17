from django import forms
from django.utils.translation import gettext_lazy as _

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
            'date',
            'event_content',
            'participating_shops_text',
            'original',
        )


class ShopEntryForm(forms.ModelForm):

    delegation_name = forms.CharField(
        label=_("店舗代表者名"),
        max_length=31,
        required=True,
    )
    shop_name = forms.CharField(
        label=_("店舗名"),
        max_length=63,
        required=True
    )
    shop_address = forms.CharField(
        label=_("店舗住所"),
        max_length=63,
        required=True
    )
    shop_mail = forms.EmailField(
        label=_("店舗メールアドレス"),
        required=True
    )

    class Meta:
        model = models.Event
        fields = ()

"""
# TODO 一般ユーザ向け参加者登録ページのフォーム
class ParticipateEntryForm(forms.ModelForm):

    class Meta:
        model = models.Event
        fields = ()
"""