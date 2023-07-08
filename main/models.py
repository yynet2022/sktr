# -*- coding: utf-8 -*-
import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


class Seat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('名前', unique=True, max_length=128)
    comments = models.CharField('コメント', max_length=256)
    is_active = models.BooleanField('有効/無効', default=True)
    create_at = models.DateTimeField('作成時刻', default=timezone.now)

    def __str__(self):
        return "Seat<%s,%s,%s>" % (self.name, self.is_active, self.comments)


class Reserve(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # default=0
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)  # default=0
    date = models.DateField('予約日', default=timezone.now)
    is_am = models.BooleanField('午前', default=True, null=False, blank=False)
    is_pm = models.BooleanField('午後', default=True, null=False, blank=False)
    create_at = models.DateTimeField('作成時刻', default=timezone.now)

    def isAM(self):
        return self.is_am

    def isPM(self):
        return self.is_pm

    def isALL(self):
        return self.is_am and self.is_pm

    def __str__(self):
        s = "<Reserve:%s," % self.user.get_full_name()
        s += self.seat.name + ","
        s += str(self.date) + ","
        if self.isALL():
            s += '終日'
        elif self.isAM():
            s += '午前'
        elif self.isPM():
            s += '午後'
        s += ">"
        return s

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date", "is_am"],
                name="user_date_am_unique"
            ),
            models.UniqueConstraint(
                fields=["user", "date", "is_pm"],
                name="user_date_pm_unique"
            ),
            models.UniqueConstraint(
                fields=["seat", "date", "is_am"],
                name="seat_date_am_unique"
            ),
            models.UniqueConstraint(
                fields=["seat", "date", "is_pm"],
                name="seat_date_pm_unique"
            ),
        ]
