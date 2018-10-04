from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

import uuid as uuid_lib


class User(AbstractBaseUser, PermissionsMixin):
    # uuid
    uuid = models.UUIDField(default=uuid_lib.uuid4, primary_key=True, editable=False)

    # username, full name
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    full_name = models.CharField(_('氏名'), max_length=150, blank=True)

    # email
    email = models.EmailField(_('email address'), blank=True)

    # bio, icon
    bio = models.TextField(max_length=500, blank=True)
    icon = ImageSpecField(source='original',
                          processors=[ResizeToFill(250, 250)],
                          format="JPEG",
                          options={'quality': 60},
                          )

    original = models.ImageField(default="media/dice.png", upload_to="media/")

    # is staff, is active (boolean), and date joined
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # User Manager
    objects = UserManager()

    # env
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
