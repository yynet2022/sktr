# -*- coding: utf-8 -*-
from django.views import generic
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from . import apps, models
import datetime


User = get_user_model()
SKTR_FOCUS_KEY = 'sktr_focus_id'


class MonthUtils:
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
        return [t.replace(day=i+1) for i in range(self.last_day.day)]


class TopView(generic.TemplateView):
    template_name = apps.AppConfig.name + '/top.html'

    def get_context_data(self, **kwargs):
        m = MonthUtils(**self.kwargs)
        days = m.days
        abase = [None] * len(days)
        seats = models.Seat.objects.filter(is_active=True).order_by('name')

        if self.request.user.is_authenticated:
            for r in models.Reserve.objects.filter(
                    user=self.request.user, date__range=(days[0], days[-1])):
                abase[r.date.day-1] = False

        def _get_seat_reserves():
            for s in seats:
                a = abase.copy()
                for r in models.Reserve.objects.filter(
                        seat=s, date__range=(days[0], days[-1])):
                    a[r.date.day-1] = r.user
                yield {'seat': s, 'reserves': a}

        fid = None
        s = self.request.session.get(SKTR_FOCUS_KEY)
        if s is not None:
            fid = f'{s[0]}-{s[1]}-{s[2]}-{s[3]}'
            del self.request.session[SKTR_FOCUS_KEY]

        kwargs.update({
            'target_month': m.target,
            'target_days': days,
            'prev_month': m.prev_month,
            'next_month': m.next_month,
            'seat_reserves': _get_seat_reserves(),
            'focus_id': fid,
        })
        return super().get_context_data(**kwargs)


class ReserveException(Exception):
    pass


class ReserveView(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        kwargs = None
        if self.request.user.is_authenticated:
            user = self.request.user

            try:
                sid = self.kwargs.get('seatid')
                year = self.kwargs.get('year')
                month = self.kwargs.get('month')
                day = self.kwargs.get('day')

                kwargs = {'year': year, 'month': month}
                date = datetime.date(year=year, month=month, day=day)
                seat = models.Seat.objects.get(id=sid)
                lookup = {'seat': seat, 'date': date}
                s1 = '{}月{}日'.format(date.month, date.day)

                r = models.Reserve.objects.filter(**lookup)
                if r.exists():
                    s2 = r[0].seat.name
                    raise ReserveException(
                        f'{s1} の <{s2}> は、既に予約されています。')

                r = models.Reserve.objects.filter(user=user, date=date)
                if r.exists():
                    s2 = r[0].seat.name
                    raise ReserveException(
                        f'{s1} は既に <{s2}> を予約しています。')

                with transaction.atomic():
                    models.Reserve.objects.create(user=user, **lookup)
                    # 同時に予約して、ダブルブッキングになってないか確認。
                    models.Reserve.objects.get(**lookup)

                s2 = seat.name
                messages.success(self.request,
                                 f'{s1} の <{s2}> を予約しました。')
                self.request.session[SKTR_FOCUS_KEY] = (
                    str(sid), year, month, day)
            except Exception as e:
                messages.warning(self.request, '予約失敗: ' + str(e))

        return reverse('main:top', kwargs=kwargs)


class CancelView(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        kwargs = None
        if self.request.user.is_authenticated:
            user = self.request.user

            try:
                sid = ''
                year = self.kwargs.get('year')
                month = self.kwargs.get('month')
                day = self.kwargs.get('day')

                kwargs = {'year': year, 'month': month}
                date = datetime.date(year=year, month=month, day=day)
                lookup = {'user': user, 'date': date}

                with transaction.atomic():
                    r = models.Reserve.objects.filter(**lookup)
                    if r.exists():
                        sid = r[0].seat.id
                        r.delete()

                s1 = '{}月{}日'.format(date.month, date.day)
                messages.success(self.request,
                                 f'{s1} の予約をキャンセルしました。')
                self.request.session[SKTR_FOCUS_KEY] = (
                    str(sid), year, month, day)
            except Exception as e:
                messages.warning(self.request, 'キャンセル失敗: ' + str(e))

        return reverse('main:top', kwargs=kwargs)
