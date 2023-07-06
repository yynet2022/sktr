# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from django import forms
from . import apps, models
import datetime


User = get_user_model()


class MonthMixin:
    def __init__(self, year=None, month=None, **kwargs):
        if year is None or month is None:
            self.target = datetime.date.today().replace(day=1)
        else:
            self.target = datetime.date(year=year, month=month, day=1)

    @property
    def prev_month(self):
        t = self.target
        if t.month == 1:
            return t.replace(year=t.year-1, month=12, day=1)
        else:
            return t.replace(month=t.month-1, day=1)

    @property
    def next_month(self):
        t = self.target
        if t.month == 12:
            return t.replace(year=t.year+1, month=1, day=1)
        else:
            return t.replace(month=t.month+1, day=1)

    @property
    def last_day(self):
        return self.next_month - datetime.timedelta(days=1)

    @property
    def days(self):
        t = self.target
        return [t.replace(day=t.day+i) for i in range(self.last_day.day)]


class TopView(generic.FormView):
    template_name = apps.AppConfig.name + '/top.html'

    def get_form(self, form_class=None):
        class _Form(forms.Form):
            pass

        return _Form(**self.get_form_kwargs())

    def get_success_url(self):
        return reverse('main:top')

    def get_context_data(self, **kwargs):
        q = MonthMixin(**self.kwargs)
        days = q.days
        arr = [None,] * len(days)
        seats = models.Seat.objects.filter(is_active=True)

        def _get_seat_list():
            for s in seats:
                a = arr.copy()
                for q in models.Reserve.objects.filter(
                        seat=s, date__range=(days[0], days[-1])):
                    a[q.date.day-1] = q.user
                yield {'seat': s.name, 'q': a}

        kwargs.update({
            'target_month': q.target,
            'target_days': days,
            'prev_month': q.prev_month,
            'next_month': q.next_month,
            'seat_list': _get_seat_list(),
        })
        return super().get_context_data(**kwargs)
