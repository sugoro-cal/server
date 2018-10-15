from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from .forms import ProfileUpdateForm


User = get_user_model()


class OnlyUserMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class ProfileView(OnlyUserMixin, DetailView):
    model = User
    template_name = 'users/user_profile.html'


class ProfileUpdateView(OnlyUserMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = "users/profile_update.html"

    def get_success_url(self):
        return reverse_lazy("profile", kwargs={"pk": self.request.user.pk})
