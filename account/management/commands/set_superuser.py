# -*- coding: utf-8 -*-
import sys
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

__all__ = ['Command']


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--%s" % 'uid',
            help="Specifies the login for the superuser.",
        )

    def handle(self, *args, **kwargs):
        try:
            uid = kwargs.get('uid', None)
            if uid is None:
                print('Users:')
                for u in User.objects.all():
                    print('  ', u)
            else:
                print("UID:", uid)
                user = User.objects.get(uid=uid)
                user.is_superuser = True
                user.is_active = True
                user.save()
                print('  ', user)
            print("done.")
        except Exception as e:
            print('Error,', e, file=sys.stderr)
            sys.exit(1)
