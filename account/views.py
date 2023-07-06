# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from . import apps, forms


User = get_user_model()


class LoginView(generic.FormView):
    template_name = apps.AppConfig.name + '/login.html'
    form_class = forms.InputUIDForm
    success_url = reverse_lazy('main:top')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["form"].initial = {'uid': self.request.user.uid}
        return context

    def form_valid(self, form):
        r = super().form_valid(form)
        uid = form.cleaned_data.get('uid', '')

        user = self.request.user
        if not user.is_authenticated or uid != user.uid:
            try:
                user = authenticate(uid=uid)
                login(self.request, user)
                messages.success(self.request, "ログインしました")
            except Exception as e:
                form.add_error('uid', "ログインに失敗しました: " + str(e))
                context = self.get_context_data(form=form)
                context["form"].initial = {'uid': uid}
                return self.render_to_response(context)
        return r


def LogoutView(request):
    logout(request)
    return redirect('main:top')
