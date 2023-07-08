# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from . import compusers, guestusers
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
# logger.setLevel(logging.INFO)

User = get_user_model()


class UserBackend(BaseBackend):
    def authenticate(self, request, uid=None):
        try:
            user = User.objects.get(uid=uid)
        except User.DoesNotExist:
            try:
                gu = guestusers.GuestUser(uid)
                user = User.objects.create_user(uid=gu.uid)
                gu.copyto(user)
            except Exception:
                cu = compusers.COMPUser(uid)
                user = User.objects.create_user(uid=cu.uid)
                cu.copyto(user)

        user.is_active = True
        user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
