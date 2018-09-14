from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate

from .forms import SignUpForm
from users.models import User


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup/signup.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
        return render(request, 'signup/signup.html', {'form': form})
