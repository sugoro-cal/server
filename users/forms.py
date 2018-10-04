from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('username', 'bio')
