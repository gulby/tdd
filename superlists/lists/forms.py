#-*- coding: utf-8 -*-
from django import forms

class ItemForm(forms.Form):
    item_text = forms.CharField(
        widget=forms.fields.TextInput(attrs={
            'placeholder': u'작업 아이템 입력',
            'class': 'form-control input-lg',
        })
    )
    