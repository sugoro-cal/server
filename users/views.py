from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView


User = get_user_model()


class OnlyUserMixin(UserPassesTestMixin):
    def test_func(self):
        # 今ログインしてるユーザーのpkと、そのユーザー情報ページのpkが同じか、又はスーパーユーザーなら許可
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class ProfileView(DetailView, OnlyUserMixin):
    model = User
    template_name = 'users/user_profile.html'

