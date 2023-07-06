# -*- coding: utf-8 -*-
from django import forms


class InputUIDForm(forms.Form):
    uid = forms.CharField(label='UserID')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['uid'].widget.attrs.update({'autofocus': True})
