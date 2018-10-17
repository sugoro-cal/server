from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

User = get_user_model()


class Event(models.Model):
    # registration status
    REGISTRATION_SHOPS = "RS"
    REGISTRATION_USERS = "RU"
    FINISH_REGISTRATION = "FR"
    EVENT_FINISHED = "EF"
    REGISTRATION_STATE_CHOICES = (
        (REGISTRATION_SHOPS,  "REGISTRATION_SHOPS"),
        (REGISTRATION_USERS,  "REGISTRATION_USERS"),
        (FINISH_REGISTRATION, "FINISH_REGISTRATION"),
        (EVENT_FINISHED, "EVENT_FINISHED"),
    )
    # state for registering
    registration_state = models.CharField(
        max_length=2,
        choices=REGISTRATION_STATE_CHOICES,
        default=REGISTRATION_SHOPS
    )

    # event's name, mail
    event_name = models.CharField(_("イベント名"), max_length=63, help_text='イベント名を入力してください', default="")
    mail = models.EmailField(_('メールアドレス'), help_text='メールアドレスを入力してください', default="")

    # location, date
    address = models.CharField(_("住所"), max_length=127, help_text='集合場所の住所を入力してください', default="")
    date = models.DateField(_("イベント開催日"), help_text='イベントの開催日を入力してください', null=True)

    # event introduction
    event_content = models.TextField(_('イベント内容'), default="", max_length=500, help_text='イベントの内容を文章で入力してください',)

    # image original, showed image
    original = models.ImageField(
        _("掲載写真"),
        upload_to="events/",
        null=True,
        help_text="イベントの詳細ページに載せる写真を登録してください"
    )
    posted = ImageSpecField(
        source='original',
        processors=[ResizeToFill(600, 800)],
        format="JPEG",
        options={'quality': 80},
    )
    slide = ImageSpecField(
        source='original',
        processors=[ResizeToFill(300, 350)],
        format="JPEG",
        options={'quality': 70},
    )

    # participating users, host user
    participating_users = models.ManyToManyField(User, blank=True, related_name="participating_users")
    host_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="hosts")

    # shops
    participating_shops_text = models.TextField(_("参加店舗一覧"), max_length=500, default="")


class Shop(models.Model):
    delegation_name = models.CharField(
        _("店舗代表者名"),
        max_length=31
    )
    shop_name = models.CharField(
        _("店舗名"),
        max_length=63,
    )
    shop_address = models.CharField(
        _("店舗住所"),
        max_length=63
    )
    shop_mail = models.EmailField(
        _("店舗メールアドレス"),
        blank=True
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        related_name='registration_shops',
        null=True
    )
