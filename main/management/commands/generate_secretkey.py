# -*- coding: utf-8 -*-
import sys
from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key

__all__ = ['Command']


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            secret_key = get_random_secret_key()
            print("SECRET_KEY = 'sktr#{}'".format(secret_key))
        except Exception as e:
            print('Error,', e, file=sys.stderr)
            sys.exit(1)
