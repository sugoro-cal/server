from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy

from . import models, forms


def index(request):
    param = {
        'events': models.Event.objects.all(),
    }
    return render(request, 'index.html', param)


class EventInfoView(DetailView):
    model = models.Event
    template_name = "app/event_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.request.GET
        return context


class RegisterForShopsView(CreateView):
    template_name = "app/register_event_datas.html"
    form_class = forms.EventRegisterForShopForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            event = models.Event(
                event_name=form.cleaned_data.get("event_name"),
                mail=form.cleaned_data.get("mail"),
                address=form.cleaned_data.get("address"),
                date=form.cleaned_data.get("date"),
                event_content=form.cleaned_data.get("event_content"),
                host_user=request.user
            )
            event.save()
            return redirect("event_info", event.id)
        return render(request, self.template_name, {'form': form})


class EventInfoUpdateView(UpdateView):
    template_name = 'app/register_event_datas.html'
    form_class = forms.EventRegisterForParticipateForm
    model = models.Event

    def get_success_url(self):
        return reverse_lazy("event_info", kwargs={"pk": self.kwargs["pk"]})


class RegisterForParticipatesView(UpdateView):

    template_name = 'app/register_event_datas.html'
    form_class = forms.EventRegisterForParticipateForm
    model = models.Event

    def get_success_url(self):
        return reverse_lazy("event_info", kwargs={"pk": self.kwargs["pk"]})

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        event.registration_state = event.REGISTRATION_USERS
        event.save()
        return super().post(request, *args, **kwargs)

