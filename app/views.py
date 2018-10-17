from django.shortcuts import render, redirect
from django.views.generic import (
    CreateView, UpdateView, DetailView
)
from django.urls import reverse_lazy

from . import models, forms


def index(request):
    param = {
        'events': models.Event.objects.all(),
    }
    return render(request, 'index.html', param)


def explain(request):
    return render(request, 'explain.html')


def error_404(request):
    return render(request, '404.html', status=404)


class EventInfoView(DetailView):
    model = models.Event
    template_name = "app/event_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = kwargs["object"]
        context["shops"] = models.Shop.objects.filter(event_id=event.id)
        year, month, day = str(event.date).split("-")
        context.update({"year": year, "month": month, "day": day})
        context["IS_ABLE_MAKING_MAP_STATES"] = [
            event.REGISTRATION_USERS,
            event.FINISH_REGISTRATION,
            event.EVENT_FINISHED
        ]
        return context


class RegisterShopsView(CreateView):
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
            return redirect("app:event_info", event.id)
        return render(request, self.template_name, {'form': form})


class EventInfoUpdateView(UpdateView):
    template_name = 'app/register_event_datas.html'
    form_class = forms.EventRegisterForParticipateForm
    model = models.Event

    def get_success_url(self):
        return reverse_lazy("app:event_info", kwargs={"pk": self.kwargs["pk"]})


class RegisterParticipatesView(UpdateView):
    template_name = 'app/register_event_datas.html'
    form_class = forms.EventRegisterForParticipateForm
    model = models.Event

    def get_success_url(self):
        return reverse_lazy("app:event_info", kwargs={"pk": self.kwargs["pk"]})

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        event.registration_state = event.REGISTRATION_USERS
        event.save()
        return super().post(request, *args, **kwargs)


class ShopEntryView(UpdateView):
    template_name = "app/shop_entry.html"
    form_class = forms.ShopEntryForm
    model = models.Event

    def get_success_url(self):
        return reverse_lazy('app:event_info', kwargs={"pk": self.kwargs["pk"]})

    def post(self, request, *args, **kwargs):
        event = self.model.objects.get(pk=self.kwargs["pk"])
        form = self.form_class(data=request.POST)
        param = {'form': form, 'pk': event.id}

        if form.is_valid():
            shop_name = form.cleaned_data.get('shop_name')
            shop_mail = form.cleaned_data.get('shop_mail')
            shops_name_valid = models.Shop.objects.filter(
                event_id=event.id,
                shop_name=shop_name,
            )
            shops_mail_valid = models.Shop.objects.filter(
                event_id=event.id,
                shop_mail=shop_mail,
            )

            if shops_name_valid:
                param['name_valid_mess'] = '同じ名前の店舗がすでに登録されています'
                return render(request, self.template_name, param)
            if shops_mail_valid:
                param['mail_valid_mess'] = '同じメールアドレスの店舗がすでに登録されています'
                return render(request, self.template_name, param)

            shop = models.Shop(
                delegation_name=form.cleaned_data.get('delegation_name'),
                shop_name=shop_name,
                shop_address=form.cleaned_data.get('shop_address'),
                shop_mail=form.cleaned_data.get('shop_mail'),
                event=event
            )
            shop.save()
            event.participating_shops_text += (shop_name+"&")
            event.save()
            return redirect("app:event_info", event.id)

        return render(request, self.template_name, param)


def participate_entry(request, pk):
    if request.method == "GET":
        return render(request, "app/participate_entry.html", {"pk": pk})
    else:
        user = request.user
        event = models.Event.objects.get(pk=pk)
        event.participating_users.add(user)
        return redirect("app:event_info", pk=pk)
