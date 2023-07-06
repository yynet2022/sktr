# -*- coding: utf-8 -*-
import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()
ATYPE_AM = 1
ATYPE_PM = 2
ATYPE_ALL = 3


class Seat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('名前', unique=True, max_length=128)
    comments = models.CharField('コメント', max_length=256)
    is_active = models.BooleanField('有効/無効', default=True)
    create_at = models.DateTimeField('作成時刻', default=timezone.now)

    def __str__(self):
        return "Seat<%s,%s,%s>" % (self.name, self.is_active, self.comments)


class Reserve(models.Model):
    ATYPE_CHOICES = (
        (ATYPE_AM,   '午前'),
        (ATYPE_PM,   '午後'),
        (ATYPE_ALL,  '終日'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # default=0
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)  # default=0
    date = models.DateField('予約日', default=timezone.now)
    atype = models.IntegerField('AM/PM/終日',
                                default=ATYPE_ALL, choices=ATYPE_CHOICES)
    create_at = models.DateTimeField('作成時刻', default=timezone.now)

    def isAM(self):
        return self.atype == ATYPE_AM

    def isPM(self):
        return self.atype == ATYPE_PM

    def isALL(self):
        return self.atype == ATYPE_ALL

    def __str__(self):
        s = "<Reserve:%s," % self.user.get_full_name()
        s += self.seat.name + ","
        s += str(self.date) + ","
        s += self.get_atype_display() + ">"
        return s
